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


async def park_auto_sm(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://park-auto-sm.ru/avto-new/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brands__card"})
    res = []
    for tag in tags:
        link_1 = 'https://park-auto-sm.ru' + tag.get("href")
        time.sleep(1)
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card"})
        for card in cards:
            try:
                link = 'https://park-auto-sm.ru' + card.find("a").get("href")
                title = card.find(attrs={"class": "mini-card__title"}).text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "new text-primary"}).text
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
            except Exception:
                pass
    return res


async def ac_triumph(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ac-triumph.ru/cars-new/?page=100'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "card-body"})
    res = []
    for card in cards:
        link = 'https://ac-triumph.ru' + card.find(attrs={"class": "card-title__link"}).get("href")
        title = card.find(attrs={"class": "card-title__title"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
        cost__ = card.find(attrs={"class": "price-box__current"}).text
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


async def ace_auto_63(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ace-auto-63.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "brand-section__item-wrap"})
    res = []
    for card in cards:
        link = card.get("href")
        title = card.find(attrs={"class": "catalog-item__name"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
        cost__ = card.find(attrs={"class": "catalog-item__price"}).text
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
