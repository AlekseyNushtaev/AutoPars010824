import csv
import json
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



def ac_neva(dct_up, browser):
    res = []
    link = 'https://ac-neva.ru/newauto/'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "brand__link"})
    for br in brands:
        link_brand = 'https://ac-neva.ru' + br.get('href')
        browser.get(link_brand)
        time.sleep(2)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "new-list__card"})
        for card in cards:
            link = 'https://ac-neva.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "new-list__name"}).find("a").text.lower().strip().replace("(ваз)", "")
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
            cost__ = card.find(attrs={"class": "new-list__price"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            try:
                name = dct_up[name]
            except KeyError:
                # await bot.send_message(CHANEL_ID, f'{name} {link}')
                print([name, cost, link])
            res.append([name, cost, link])
            # print([name, cost, link])
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
res = ac_neva(dct, browser)
print(len(res))

