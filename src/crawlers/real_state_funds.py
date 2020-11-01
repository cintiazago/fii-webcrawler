import time
import requests
import pandas as pd
import pandera as pa
import json
import traceback
import datetime
import decimal
import logging
import sys, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from unicodedata import normalize

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import settings
import exceptions

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def clean_normalize(data):
    """
    Normalize unicode characters, strip trailing spaces
    and recalculate the numerics columns.
    """
    if isinstance(data, str):
        return normalize('NFKC', data).strip()
    if isinstance(data, float):
        return data / 100
    else:
        return data

class BotFIIsWebsite():
    def __init__(self):
        """
        Constructor
        """
        self.url_to_parse = settings.URL_TO_PARSE
        self.wait_time_in_seconds = int(settings.REQUEST_WAIT_TIME_IN_SECONDS)
        self.option = Options()
        self.option.headless = bool(settings.WEB_DRIVER_OPTION_HEADLESS)
        self.driver = webdriver.Firefox(options=self.option)

    def _get_html_content(self):
        """
        Get the URL of the HTML and returns the full content
        """
        logging.info('Geting the HTML content from %s' % self.url_to_parse)
        self.driver.get(self.url_to_parse)
        time.sleep(self.wait_time_in_seconds)
        element = self.driver.find_element_by_xpath(
            f"//div[@class='dataTables_scrollBody']//table")
        html_content = element.get_attribute('outerHTML')
        if not html_content or \
            'Nenhum registro encontrado' in html_content:
            logging.error('Output with no valid content')
            raise exceptions.FileWithNoContentException(
                400,
                "Cant parse an empty output.")
        # print(html_content)
        return html_content

    def _parse_content(self, content):
        """
        Parse the content to a especific dictionary and return the json
        """
        logging.info('Parsing HTML content')
        if not content:
            logging.error('Output with no valid content')
            raise exceptions.FileWithNoContentException(
                400,
                "Cant parse an empty output.")
        soup = BeautifulSoup(content, 'lxml')
        table = soup.find(name='table')
        logging.info('Reading HTML table with requested data')

        # Filtering the first 400 elements on table to optimize memory
        data_frame_full = pd.read_html(str(table))[0].head(400)

        logging.info('Quiting Firefox')
        self.driver.quit()
        self.driver = None

        data_frame = data_frame_full[[
            'Ticker', 'Administrador', 'Último Rend. (R$)', 'Último Rend. (%)',
            'Cotação/VP', 'Cota base']]
        data_frame.columns = [
            'ticker', 'administrador', 'ultimo_rend', 'ultimo_rend_perc',
            'p_vp', 'cota_base']

        # This step is needed to fulfill columns with NaN values
        # The inplace parameter says that the current object will be changed
        # within generate another copy of the original object
        data_frame.fillna(0, inplace=True)

        logging.info('Sanitizing fields')
        validated_data_frame = self._validate_schema(data_frame)
        sanitized_data_frame = validated_data_frame.applymap(clean_normalize)

        return json.dumps(
            sanitized_data_frame.to_dict('records'), cls=JSONEncoder)

    @staticmethod
    def _validate_schema(data_frame):
        logging.info('Validating Data Frame Schema')
        schema = pa.DataFrameSchema({
            "ticker": pa.Column(str, nullable=False, required=True),
            "administrador": pa.Column(str),
            "ultimo_rend": pa.Column(float, nullable=False, coerce=True),
            "ultimo_rend_perc": pa.Column(float, nullable=True),
            "p_vp": pa.Column(float, nullable=True),
            "cota_base": pa.Column(float, nullable=True),
        })
        validated_data_frame = schema.validate(data_frame)
        return validated_data_frame

    @staticmethod
    def _export_local_file(output):
        if output:
            logging.info('Exporting JSON with the data parsed')
            with open('output.json', 'w') as f:
                f.write(output)
        else:
            logging.error(
                'JSON File could not be saved because there is no content')

    def _send_to_api(self, data):
        """
        Send the output generated to the API
        """
        pass

    def start(self):
        """
        Start the process of web scraping
        """
        try:
            content = self._get_html_content()
            parsed_content = self._parse_content(content)
            self._export_local_file(parsed_content)
            self._send_to_api(parsed_content)
            logging.info('Web scraping finished successfully!')
        except exceptions.FileWithNoContentException as e:
            logging.error("[%s] %s" % (e.code, e.message))
        except Exception as e:
            logging.error("[%s] %s" % ('500', str(e)))
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
