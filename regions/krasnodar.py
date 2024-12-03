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

async def krd_93_auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://krd93-auto.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://krd93-auto.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def car_kranodar(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://car-krasnodar.ru/cars/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "brand__item"})
    res = []
    for br in brands:
        link_1 = 'https://car-krasnodar.ru' + br.find("a").get("href")
        time.sleep(0.2)
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card__body"})
        for card in cards:
            link = 'https://car-krasnodar.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "card__special-name"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "card__price-main"}).text
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


async def avangard_yug(dct_up, browser):
    link = 'https://avangard-yug.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car__item-content"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find("a").text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "car__price"}).find(attrs={"class": "car__price-inner"}).text
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


async def ac_pegas(dct_up, browser):
    link = 'https://ac-pegas.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item__baselink"})
    res = []
    for card in cards:
        link = card.get("href")
        title = card.find(attrs={"class": "main_catalog_item__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "main_catalog_item__creditprice"}).text
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


async def rostov_avto(dct_up, browser):
    link = 'https://rostov-avto-1.ru/'
    browser.get(link)
    time.sleep(5)
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
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, cost, link])
    return res


async def loft_autoug(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://loft-autoug.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "category__item-wrapper"})
    res = []
    for br in brands:
        link_1 = 'https://loft-autoug.ru' + br.find("a").get("href")
        brand = br.find("a").get("href").strip().split('/')[-1]
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "product__item"})
        for card in cards:
            link = 'https://loft-autoug.ru' + card.find("a").get("href")
            model = card.find(attrs={"class": "product__item-title"}).find("a").text.lower().strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "price_validation"}).text
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


async def krd_93_car(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://krd93-car.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://krd93-car.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res
