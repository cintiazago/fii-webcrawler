import time
import requests
import pandas as pd
import json
import traceback
import datetime
import decimal
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from unicodedata import normalize

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

class BotRealStateFunds():
    def __init__(self):
        """
        Constructor
        """
        self.url_to_parse = settings.URL_TO_PARSE
        self.wait_time_in_seconds = int(settings.WAIT_TIME_IN_SECONDS)
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox()

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
        # print(html_content)
        if not html_content or \
            'Nenhum registro encontrado' in html_content:
            logging.error('Output with no valid content')
            raise exceptions.FileWithNoContentException(
                400,
                "Cant parse an empty output.")
        return html_content if html_content else None

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
        data_frame_full = pd.read_html(str(table))[0].head(300)
        data_frame = data_frame_full[[
            'Ticker', 'Administrador', 'Último Rend. (R$)', 'Último Rend. (%)',
            'Cotação/VP', 'Cota base']]
        data_frame.columns = [
            'ticker', 'administrador', 'ultimo_rend', 'ultimo_rend_perc',
            'p_vp', 'cota_base']
        logging.info('Quiting Firefox')
        self.driver.quit()
        self.driver = None
        logging.info('Sanitizing fields')
        data_frame = data_frame.applymap(clean_normalize)
        return json.dumps(data_frame.to_dict('records'), cls=JSONEncoder)

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
            logging.error("ERROR: [%s] %s" % (e.code, e.message))
        except Exception:
            logging.error("ERROR: [%s] %s" % (e))
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
