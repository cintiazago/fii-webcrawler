import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


# 1. Pegar o conteúdo HTML a partir da URL
url = "https://fiis.com.br/lupa-de-fiis/"
real_states_funds = {}

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)

time.sleep(5)

try:
    element = driver.find_element_by_xpath(f"//div[@class='dataTables_scrollBody']//table")
    html_content = element.get_attribute('outerHTML')

except Exception:
    pass

# 2. Parsear o conteúdo HTML - BeautifulSoup
try:
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # 3. Transformar os dados em um Dicionário de dados próprio
    df_full = pd.read_html(str(table))[0].head(200)
    df = df_full[['Ticker', 'Último Rend. (R$)', 'Último Rend. (%)']]
    df.columns = ['ticker', 'ultimo_rend', 'ultimo_rend_perc']

    driver .quit()

    # 4. Converter e salvar em um arquivos JSON
    output = json.dumps(df.to_dict('records'))
    with open('output.json', 'w') as f:
        f.write(output)

    # 5. Enviar para a API

except Exception:
    pass
finally:
    print('Web scraping finished!')
