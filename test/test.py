import time
import requests
import bs4
import fake_headers
from selenium.webdriver.common.by import By

from bot import bot
from config import ADMIN_ID, CHANEL_ID
from pprint import pprint

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


def mnogo_auto_174(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://mnogo-auto174.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://kc-klassavto.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            print(name, link)
            # await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
        print([name, dct["cost"], link])

    return res

# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = mnogo_auto_174(dct)
print(len(res))