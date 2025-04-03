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



def vzletka(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://cartrade-vzletka.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "marks-grid"}).find_all("a")
    print(len(tags))
    res = []
    for tag in tags:
        cnt = 1
        while True:
            link_1 = tag.get("href") + f'?page={cnt}'
            response = requests.get(link_1, headers.generate())
            time.sleep(0.25)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'lxml')
            cards = soup.find_all(attrs={"class": "car-card"})
            if len(cards) == 0:
                break
            for card in cards:
                title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                name = brand + ', ' + model
                try:
                    name = dct_up[name]
                except KeyError:
                    print(name)
                res.append(name)
                print(name)
            cnt += 1
    return res


chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1200,600")

options.add_argument('--disable-dev-shm-usage')
browser = Chrome(service=browser_service, options=options)
browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = vzletka(dct, browser)
print(len(res))

wb = openpyxl.load_workbook('../models_tech.xlsx')
sh = wb['Sheet']
for i in range(2, 249):
    brand = sh.cell(i, 3).value
    model = sh.cell(i, 4).value
    name = brand + ', ' + model
    if name in res:
        sh.cell(i, 16).value = 'Да'
wb.save('../models_tech.xlsx')
