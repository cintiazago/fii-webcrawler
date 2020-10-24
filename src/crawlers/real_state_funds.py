import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import traceback
import datetime
import decimal

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
        Get the URL of the HTML returns the full content
        """
        self.driver.get(self.url_to_parse)
        time.sleep(self.wait_time_in_seconds)
        try:
            element = self.driver.find_element_by_xpath(
                f"//div[@class='dataTables_scrollBody']//table")
            html_content = element.get_attribute('outerHTML')
            print(html_content)
            if not html_content:
                raise exceptions.FileWithNoContentException(
                    404,
                    "Cant parse an empty outuput.")
            return html_content if html_content else None
        except Exception:
            traceback.print_exc()

    def _parse_content(self, content):
        """
        Parse the content to a especific dictionary and return the json
        """
        if not content:
            raise exceptions.FileWithNoContentException(
                404,
                "Cant parse an empty outuput.")
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find(name='table')
        data_frame_full = pd.read_html(str(table))[0].head(200)
        data_frame = data_frame_full[[
            'Ticker', 'Último Rend. (R$)', 'Último Rend. (%)']]
        data_frame.columns = [
            'ticker', 'ultimo_rend', 'ultimo_rend_perc']
        self.driver.quit()
        return json.dumps(data_frame.to_dict('records'), cls=JSONEncoder)

    @staticmethod
    def _export_local_file(output):
        if output:
            with open('output.json', 'w') as f:
                f.write(output)
        else:
            print("No file was exported.")

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
            print('Web scraping finished successfully!')
        except Exception:
            traceback.print_exc()
