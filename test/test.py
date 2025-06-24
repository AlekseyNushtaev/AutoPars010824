import csv
import json
import time

import openpyxl
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




def vita_avto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://vita-auto.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "catalogTop_item"})
    res = []
    print(len(brands))
    for brand_ in brands:
        time.sleep(0.2)
        brand = brand_.find(attrs={"class": "nameCar"}).text.strip().lower()
        link_1 = 'https://vita-auto.ru' + brand_.find("a").get("href")
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "CATALOG_items"}).find_all(attrs={"class": "CATALOG_item"})
        print(len(cards))
        for card in cards:
            link = 'https://vita-auto.ru' + card.find(attrs={"class": "CATALOG_item_imageCar_img_link"}).get("href")
            model = card.find(attrs={"class": "CATALOG_item_detail_content_nameCar"}).text.lower().strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "CATALOG_item_detail_content_price"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            try:
                name = dct_up[name]
            except KeyError:
                pass
                # await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
    return res


# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
#
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)
# browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = vita_avto(dct)
print(len(res))
