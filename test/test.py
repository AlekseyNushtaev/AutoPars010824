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




def kanavto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    count = 1
    dct = {}
    while True:
        time.sleep(0.2)
        link_1 = f'https://kanavto.ru/new/?page={count}'
        response = requests.get(link_1, headers.generate(), verify=False)
        count += 1
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card height"})
        if len(cards) == 0:
            break
        for card in cards:
            try:
                title = card.find(attrs={"class": "card-name"}).text.lower().strip()
                link = card.get("href")
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
                cost__ = card.find(attrs={"class": "card-price"}).text
                cost_ = ''
                for y in cost__:
                    if y.isdigit():
                        cost_ += y
                cost = int(cost_)
                name = brand + ', ' + model
                if name not in dct.keys():
                    dct[name] = [cost, link]
                else:
                    cost_old = dct[name][0]
                    if cost < cost_old:
                        dct[name] = [cost, link]
            except Exception as e:
                print(e)
    res = []
    for key in dct.keys():
        name = key
        try:
            name = dct_up[name]
        except KeyError:
            print(f'{name} {dct[key][1]}')
        res.append([name, dct[key][0], dct[key][1]])
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
res = kanavto(dct)
print(len(res))
