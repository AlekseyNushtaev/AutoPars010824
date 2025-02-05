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


def rostov_avto(dct_up, browser):
    link = 'https://rostov-avto-1.ru/'
    browser.get(link)
    time.sleep(10)
    flag = True
    while flag:
        flag = False
        buttons = browser.find_elements(
            By.TAG_NAME,
            'tr')
        for button in buttons:
            if "загрузить еще" in button.text.lower().strip():
                button.click()
                flag = True
                time.sleep(5)
                break
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "js-product t-store__card t-store__stretch-col t-store__stretch-col_33 t-align_left t-item"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "js-store-prod-name js-product-name t-store__card__title t-typography__title t-name t-name_md"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "js-product-price js-store-prod-price-val t-store__card__price-value"}).text
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
res = rostov_avto(dct, browser)
print(len(res))
