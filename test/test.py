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



def saratov_autospot(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov.autospot.ru/brands/'
    response = requests.get(link, headers.generate())
    time.sleep(0.5)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"data-testid": "allBrands-block"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://saratov.autospot.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.5)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "brand-model-catalog"}).find_all(attrs={"class": "brand-model-card"})
        for card in cards:
            link = 'https://saratov.autospot.ru' + card.find("a").get("href")
            title = card.find("a").text.replace(' • ', ' ').lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            try:
                cost__ = card.find(attrs={"class": "brand-model-card__price-sale"}).text.strip()
            except:
                cost__ = card.find(attrs={"class": "brand-model-card__price"}).text.strip()
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
            except:
                print([name, cost, link])
                # await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
            print([name, cost, link])
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
res = saratov_autospot(dct)
print(len(res))
