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


async def saratov_avtohous(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov-avtohous.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "mark--logo-item"})
    res = []
    for tag in tags:
        link_1 = tag.get("href")
        time.sleep(1)
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "car__item"})
        for card in cards:
            link = card.find("a").get("href")
            title = card.find(attrs={"class": "car__item__name"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "price"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            try:
                name = dct_up[name]
            except KeyError:
                await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
    return res

# res = saratov_avtohous({})
# res_name = []
# with open('../autolist.txt', 'r', encoding='utf-8') as f:
#     lst = f.readlines()
#     for item in lst:
#         res_name.append(item.split('|')[0].strip())
# for i in res:
#     if i[0] not in res_name:
#         print(i)