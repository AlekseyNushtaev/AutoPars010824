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


def saturn2(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://tumencars.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    print(soup.prettify())
#     brands = soup.find(attrs={"class": "nav__item"}).find_all(attrs={"class": "nav__item-drop"})
#     print(len(brands))
#     res = []
#     for brand in brands:
#         link = 'https://saturn2.ru' + brand.find("a").get("href")
#         browser.get(link)
#         time.sleep(10)
#         html = browser.page_source
#         soup = bs4.BeautifulSoup(html, 'lxml')
#         cards = soup.find(attrs={"class": "post-wrapper__grid"}).find_all(attrs={"class": "post-preview"})
#         print(len(cards))
#         for card in cards:
#             try:
#                 link = 'https://saturn2.ru' + card.find("a").get("href")
#                 title = card.find(attrs={"class": "post-preview__row"}).find(attrs={"class": "post-preview__name"}).text.lower().strip().replace(",", "")
#                 marka = title.split()[0]
#                 model = title.replace(marka, '').strip().replace(" ", "")
#                 cost__ = card.find(attrs={"class": "post-preview__price"}).text
#                 cost_ = ''
#                 for y in cost__:
#                     if y.isdigit():
#                         cost_ += y
#                 cost = int(cost_)
#                 name = marka + ', ' + model
#                 try:
#                     name = dct_up[name]
#                 except KeyError:
#                     pass
#                     # await bot.send_message(CHANEL_ID, f'{name} {link}')
#                 res.append([name, cost, link])
#             except Exception:
#                 continue
#     return res
#
#
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
res = saturn2(dct)
# print(len(res))
