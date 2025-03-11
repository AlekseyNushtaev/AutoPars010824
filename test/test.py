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


def astella_cars(dct_up):
    link = 'https://ufa.masmotors.ru/catalog/omoda'
    response = requests.get(link)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    print(soup.prettify())
    # brands = soup.find(attrs={"class": "brands-menu"}).find_all("a")
    # res = []
    # for brand_ in brands:
    #     link_1 = brand_.get("href")
    #     browser.get(link_1)
    #     time.sleep(2)
    #     html = browser.page_source
    #     soup = bs4.BeautifulSoup(html, 'lxml')
    #     try:
    #         cards = soup.find(attrs={"class": "cars-block"}).find_all(attrs={"class": "cars-block__item-col cars-block__item-info"})
    #     except AttributeError:
    #         continue
    #     for card in cards:
    #         link = card.find(attrs={"class": "catalog-item__model link-black"}).get("href")
    #         title = card.find(attrs={"class": "h3__brand"}).text.lower().strip()
    #         brand = title.split()[0]
    #         model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
    #         cost__ = card.find(attrs={"class": "catalog-item__price-current js_model-i-price"}).text
    #         cost_ = ''
    #         for y in cost__:
    #             if y.isdigit():
    #                 cost_ += y
    #         cost = int(cost_)
    #         name = brand + ', ' + model
    #         try:
    #             name = dct_up[name]
    #         except KeyError:
    #             await bot.send_message(CHANEL_ID, f'{name} {link}')
    #         res.append([name, cost, link])
    # return res




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
res = astella_cars(dct)
print(len(res))
