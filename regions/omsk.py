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


async def vostoc_ac(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://vostok-ac.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://vostok-ac.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])

    return res


async def center_irtysh(dct_up, browser):
    link = 'https://center-irtysh.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog-item"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "catalog-item-title"}).get("href")
        title = card.find(attrs={"class": "catalog-item-title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "catalog-item-info__pricing__new"}).text
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


async def astella_cars(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://astella-cars.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "list list__marks"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://astella-cars.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card mini-card__folder"})
        for card in cards:
            link = 'https://astella-cars.ru' + card.get("href")
            title = card.find(attrs={"class": "mini-card__folder-title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "mini-card__folder-prices"}).text.strip()
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
    return res


async def omsk_cars(dct_up, browser):
    link = 'https://omsk-cars.ru/catalog'
    browser.get(link)
    time.sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # scroll_js = "window.scrollBy(0, 1000);"
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # browser.execute_script(scroll_js)
        time.sleep(2)  # Adjust sleep duration as needed
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://omsk-cars.ru' + card.get("href")
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


async def omsk_carso(dct_up):
    link = 'https://omsk.carso.ru/newauto'
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


async def irtysh_avtosalon(dct_up):
    cnt = 1
    res = []
    while True:
        link = f'https://irtysh-avtosalon.ru/new_auto/page/{cnt}/'
        response = requests.get(link)
        time.sleep(0.2)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "auto-card new_auto"})
        if len(cards) == 0:
            break
        for card in cards:
            link = card.get("href")
            title = card.find(attrs={"class": "auto-card__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
            cost__ = card.find(attrs={"class": "auto-card__price"}).text
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
        cnt += 1
    return res
