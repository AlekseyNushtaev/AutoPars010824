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


# async def vlg_autotrade(dct_up):
#     headers = fake_headers.Headers(browser='firefox', os='win')
#     link = 'https://vlg-autotrade.ru/auto'
#     response = requests.get(link, headers.generate())
#     html = response.text
#     soup = bs4.BeautifulSoup(html, 'lxml')
#     cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
#     res = []
#     for card in cards:
#         data = card.get("data-model").replace('null', 'None').replace('\\', '')
#         dct = eval(data)
#         link = 'https://vlg-autotrade.ru' + card.find("a").get("href")
#         name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
#         try:
#             name = dct_up[name]
#         except KeyError:
#             await bot.send_message(CHANEL_ID, f'{name} {link}')
#         res.append([name, dct["cost"], link])
#     return res
#
#
# async def vlg_autostore(dct_up, browser):
#     link = 'https://volgograd-autostore.ru/catalog'
#     browser.get(link)
#     time.sleep(2)
#     SCROLL_PAUSE_TIME = 1
#
#     # Get scroll height
#     last_height = browser.execute_script("return document.body.scrollHeight")
#
#     while True:
#         # Scroll down to bottom
#         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)
#
#         # Calculate new scroll height and compare with last scroll height
#         new_height = browser.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
#     html = browser.page_source
#     soup = bs4.BeautifulSoup(html, 'lxml')
#     cards = soup.find_all(attrs={"class": "UiLink_UiLink__pbmRv UiLink CatalogCar_CatalogCar__6ku6m"})
#     res = []
#     for card in cards:
#         link = 'https://volgograd-autostore.ru' + card.get("href")
#         title = card.find(attrs={"class": "CatalogCar_CatalogCarTitle__sqMzF"}).text.lower().strip().replace("š", "s")
#         brand = title.split()[0]
#         model = title.replace(brand, '').strip().replace(" ", "")
#         cost__ = card.find(attrs={"class": "CatalogCar_CatalogCarPrice__2905b"}).text
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
#     return res


async def vlg_auto34(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://vlg-auto34.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://vlg-auto34.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res