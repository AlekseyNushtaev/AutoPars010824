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


async def lvl_auto(dct_up, browser):
    link = 'https://lvl-auto.ru/catalog/'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(5)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://lvl-auto.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
        brand = title.split()[0].replace('š', 's')
        model = title.replace(brand, '').strip().replace(" ", "").replace(' ', '').replace('škoda', '')
        price_ = card.find(attrs={"class": "car-card__price"}).text
        price = ''
        for i in price_:
            if i.isdigit():
                price += i
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res


async def globus_auto(dct_up, browser):
    link = 'https://globus-auto16.ru/catalog/'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(5)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://globus-auto16.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
        brand = title.split()[0].replace('š', 's')
        model = title.replace(brand, '').strip().replace(" ", "").replace(' ', '').replace('škoda', '')
        price_ = card.find(attrs={"class": "car-card__price"}).text
        price = ''
        for i in price_:
            if i.isdigit():
                price += i
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res


async def kazan_avtosalon(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://kazan.avtosalon.shop/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find_all(attrs={"class": "header-brands__item-link"})
    res = []
    for brand in brands:
        link_1 = 'https://kazan.avtosalon.shop' + brand.get("href")
        browser.get(link_1)
        time.sleep(2)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "item"})
        for card in cards:
            title = card.find(attrs={"class": "name mb-3 d-block"}).text.lower().strip()
            link = card.find(attrs={"class": "name mb-3 d-block"}).get("href")
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
            cost__ = card.find(attrs={"class": "d-block new"}).text
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


async def kanavto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    count = 1
    dct = {}
    while True:
        time.sleep(0.2)
        link_1 = f'https://kanavto.ru/new/?page={count}'
        response = requests.get(link_1, headers.generate(), verify=False)
        count += 1
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card height"})
        if len(cards) == 0:
            break
        for card in cards:
            try:
                title = card.find(attrs={"class": "card-name"}).text.lower().strip()
                link = card.get("href")
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
                cost__ = card.find(attrs={"class": "card-price"}).text
                cost_ = ''
                for y in cost__:
                    if y.isdigit():
                        cost_ += y
                cost = int(cost_)
                name = brand + ', ' + model
                if name not in dct.keys():
                    dct[name] = [cost, link]
                else:
                    cost_old = dct[name][0]
                    if cost < cost_old:
                        dct[name] = [cost, link]
            except Exception as e:
                print(e)
    res = []
    for key in dct.keys():
        name = key
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {dct[key][0]}')
        res.append([name, dct[key][0], dct[key][1]])
    return res


async def dialog_auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    count = 1
    dct = {}
    while True:
        time.sleep(0.2)
        link_1 = f'https://dialog-auto.ru/cars/new/?page={count}'
        response = requests.get(link_1, headers.generate(), verify=False)
        count += 1
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card"})
        if count == 80:
            break
        for card in cards:
            title = card.find(attrs={"class": "card__title"}).text.lower().strip()
            link = 'https://dialog-auto.ru' + card.find(attrs={"class": "card__title-block"}).get("href")
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|","i")
            cost__ = card.find(attrs={"class": "card__price-new"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            if name not in dct.keys():
                dct[name] = [cost, link]
            else:
                cost_old = dct[name][0]
                if cost < cost_old:
                    dct[name] = [cost, link]
    res = []
    for key in dct.keys():
        name = key
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {dct[key][0]}')
        res.append([name, dct[key][0], dct[key][1]])
    return res


async def level_motors(dct_up, browser):
    link = 'https://level-motors16.ru/catalog/'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(5)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://level-motors16.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
        brand = title.split()[0].replace('š', 's')
        model = title.replace(brand, '').strip().replace(" ", "").replace(' ', '').replace('škoda', '')
        price_ = card.find(attrs={"class": "car-card__price"}).text
        price = ''
        for i in price_:
            if i.isdigit():
                price += i
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res


async def kazan_avto(dct_up, browser):
    link = 'https://kazan-avtomobili-2025.ru/catalog'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(5)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "UiLink_UiLink__pbmRv UiLink CatalogCar_CatalogCar__6ku6m"})
    res = []
    for card in cards:
        link = 'https://kazan-avtomobili-2025.ru' + card.get("href")
        title = card.find(attrs={"class": "CatalogCar_CatalogCarTitle__sqMzF"}).text.lower().strip()
        brand = title.split()[0].replace('š', 's')
        model = title.replace(brand, '').strip().replace(" ", "").replace(' ', '').replace('škoda', '')
        price_ = card.find(attrs={"class": "CatalogCar_CatalogCarPrice__2905b"}).text
        price = ''
        for i in price_:
            if i.isdigit():
                price += i
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res


async def l_auto(dct_up, browser):
    link = 'https://l-auto16.ru/catalog/'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(5)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://l-auto16.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
        brand = title.split()[0].replace('š', 's')
        model = title.replace(brand, '').strip().replace(" ", "").replace(' ', '').replace('škoda', '')
        price_ = card.find(attrs={"class": "car-card__price"}).text
        price = ''
        for i in price_:
            if i.isdigit():
                price += i
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, price, link])
    return res


async def newavto_kazan(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://newavto-kazan.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://newavto-kazan.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res
