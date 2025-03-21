import datetime
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


async def spb_carso(dct_up):
    link = 'https://spb.carso.ru/newauto'
    response = requests.get(link)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards_ = soup.find_all(attrs={"class": "crossover-models"})
    res = []
    for card_ in cards_:
        cards = card_.find_all(attrs={"class": "swiper-slide"})
        for card in cards:
            link = 'https://spb.carso.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "best-separate__chang"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("\n", "")
            cost__ = card.find(attrs={"class": "price-car"}).text
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


async def credit_cars_spb(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://credit-cars-spb.ru/cars-new/?page=100'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card car-card--type-display"})
    res = []
    for card in cards:
        link = 'https://credit-cars-spb.ru' + card.find(attrs={"class": "card-title__link"}).get("href")
        title = card.find(attrs={"class": "card-title__title"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
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


async def renault_nnov(dct_up, browser):
    link = 'https://renault-nnov.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find(attrs={"id": "catalog"}).find_all(attrs={"class": "model model--bordered"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "model__name"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "model__price-current"}).text
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


async def altimus_auto(dct_up, browser):
    link = 'https://altimus-auto.ru/auto'
    browser.get(link)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "car__title"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "car__price"}).text
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
