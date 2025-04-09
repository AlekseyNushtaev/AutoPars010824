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



def saratov_autosalon(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov.autosalon.shop'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "header-brands__list row"}).find_all("a")
    res = []
    for tag in tags[:-1]:
        brand = tag.find(attrs={"class": "header-brands__item-text"}).text.lower().strip()
        link_1 = 'https://saratov.autosalon.shop' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "models-card__inner"})
        for card in cards:
            try:
                link = 'https://saratov.autosalon.shop' + card.get("href")
                model = card.find(attrs={"class": "models-card__name"}).text.lower().strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "models-card__price-new"}).text.strip()
                cost_ = ''
                for y in cost__:
                    if y.isdigit():
                        cost_ += y
                if cost_ == '':
                    continue
                cost = int(cost_)
                name = brand + ', ' + model
                try:
                    name = dct_up[name]
                except KeyError:
                    print([name, cost, link])
                    # await bot.send_message(CHANEL_ID, f'{name} {link}')
                res.append([name, cost, link])
                # print([name, cost, link])
            except:
                pass
    return res


# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
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
res = saratov_autosalon(dct)
print(len(res))
