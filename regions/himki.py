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


async def autogansa(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autogansa.ru/cars/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "mark__list"}).find_all(attrs={"class": "mark__item"})
    res = []
    for tag in tags:
        link_1 = 'https://autogansa.ru' + tag.find("a").get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "car-mini__item"})
        for card in cards:
            try:
                link = 'https://autogansa.ru' + card.find("a").get("href")
                title = card.find(attrs={"class": "car-mini__name-car"}).text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "car-mini__price-value"}).text.strip()
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
                except KeyError:
                    await bot.send_message(CHANEL_ID, f'{name} {link}')
                res.append([name, cost, link])
            except:
                pass
    return res