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



def autosalon_arena(dct_up, browser):
    link = 'https://autosalon-arena.ru/cars'
    browser.get(link)
    time.sleep(2)
    time.sleep(0.25)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "brand__link"})
    res = []
    for brand_ in brands:
        link_1 = 'https://autosalon-arena.ru' + brand_.get("href")
        browser.get(link_1)
        time.sleep(2)
        time.sleep(0.25)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "model__info"})
        for card in cards:
            link = 'https://autosalon-arena.ru' + card.get("href")
            title = card.find(attrs={"class": "name"}).text.lower().replace('ваз (lada)', 'lada').strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i").replace("(ваз)", "")
            cost__ = card.find(attrs={"class": "model__price-current"}).text
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


chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument("--window-size=1200,600")

options.add_argument('--disable-dev-shm-usage')
browser = Chrome(service=browser_service, options=options)
browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = autosalon_arena(dct, browser)
print(len(res))
