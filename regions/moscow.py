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

async def nord_car(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://nord-car.ru/catalog'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "cars-list__item-top"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "absolute-link"}).get("href")
        brand = link.split('/')[-2]
        model = card.find(attrs={"class": "absolute-link"}).text.strip()
        name = brand.lower() + ', ' + model.lower().replace(" ", "")
        price_ = card.find(attrs={"class": "cars-list__price"}).text
        price = ('')
        for i in price_:
            if i.isdigit():
                price += i
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res

async def dc_dbr(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://dc-dbr.ru/catalog'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "popular_car car"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "car_link"}).get("href")
        title = card.find(attrs={"class": "car_title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        try:
            cost__ = card.find(attrs={"class": "car_type_kpp"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
        except AttributeError:
            response = requests.get(link, headers.generate())
            html = response.text
            soup = bs4.BeautifulSoup(html, 'lxml')
            cost__ = soup.find(attrs={"class": "main_car_block_left_price"}).text
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


async def autos_s(dct_up, browser):
    link = 'https://autos-s.ru/auto'
    browser.get(link)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "model"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "model__img"}).get("href")
        title = card.find(attrs={"class": "model__img"}).find("img").get("alt").lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "h4 text--bold"}).text
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

async def warshauto(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://warshauto.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "car-selection__list"}).find_all("li")
    res = []
    for brand in brands:
        link_1 = brand.find("a").get("href")
        browser.get(link_1)
        time.sleep(2)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "lineup"})
        for card in cards:
            title = card.find(attrs={"class": "lineup-info"}).find("a").text.lower().strip()
            link = card.find(attrs={"class": "lineup-info"}).find("a").get("href")
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
            cost__ = card.find(attrs={"class": "lineup-price__current"}).text
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


async def kosmos_cars(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://kosmos-cars.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "car__list"}).find_all("a")
    res = []
    for brand in brands:
        time.sleep(1)
        link_1 = 'https://kosmos-cars.ru' + brand.get("href")
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "car__container"}).find_all(attrs={"class": "card"})
        for card in cards:
            link = 'https://kosmos-cars.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "car__name"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
            cost__ = card.find(attrs={"class": "car__price"}).find_all("span")[-1].text
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


async def idol_avto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://idol-avto.ru/cars-new/?page=100'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "card-body"})
    res = []
    for card in cards:
        link = 'https://idol-avto.ru' + card.find(attrs={"class": "card-title__link"}).get("href")
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


async def vita_avto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://vita-auto.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "catalogTop_item"})
    res = []
    for brand_ in brands:
        time.sleep(0.5)
        brand = brand_.find(attrs={"class": "nameCar"}).text.strip().lower()
        link_1 = 'https://vita-auto.ru' + brand_.find("a").get("href")
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "CATALOG_items"}).find_all(attrs={"class": "CATALOG_item"})
        for card in cards:
            link = 'https://vita-auto.ru' + card.find(attrs={"class": "CATALOG_item_imageCar_img_link"}).get("href")
            model = card.find(attrs={"class": "CATALOG_item_detail_content_nameCar"}).text.lower().strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "CATALOG_item_detail_content_price"}).text
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


async def alcon_avto(dct_up, browser):
    link = 'https://alcon-auto.ru'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "brands-menu"}).find_all("a")
    res = []
    for brand_ in brands:
        link_1 = brand_.get("href")
        browser.get(link_1)
        time.sleep(2)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        try:
            cards = soup.find(attrs={"class": "cars-block"}).find_all(attrs={"class": "cars-block__item-col cars-block__item-info"})
        except AttributeError:
            continue
        for card in cards:
            link = card.find(attrs={"class": "catalog-item__model link-black"}).get("href")
            title = card.find(attrs={"class": "h3__brand"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
            cost__ = card.find(attrs={"class": "catalog-item__price-current js_model-i-price"}).text
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
