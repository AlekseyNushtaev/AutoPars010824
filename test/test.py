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



def fast_autodealer(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    cnt = 1
    res = []
    while True:
        time.sleep(0.5)
        link = f'https://fast-autodealer.ru/new_auto/page/{cnt}/'
        response = requests.get(link, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        try:
            cards = soup.find_all(attrs={"class": "auto-card new_auto"})
        except Exception:
            break
        if len(cards) == 0:
            break
        for card in cards:
            link = card.get("href")
            title = card.find(attrs={"class": "auto-card__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "auto-card__price"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            try:
                name = dct_up[name]
            except KeyError:
                print([name, cost, link])
                # await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
            print([name, cost, link])
        cnt += 1
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
res = fast_autodealer(dct)
print(len(res))
