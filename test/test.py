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


def kia_novo(dct_up, browser):
    link = 'https://kia-novo.ru/'
    browser.get(link)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = 'kia ' + card.find(attrs={"class": "main_catalog_item__title"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "main_catalog_item__price"}).find("div").text
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
            pass
        res.append([name, cost, link])
        print([name, cost, link])
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
res = kia_novo(dct, browser)
print(len(res))
