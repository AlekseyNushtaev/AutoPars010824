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


async def autocentr72(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autocentr-72.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autocentr-72.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def bazis_motor(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://bazis-motors.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "dropdown_list brand_logos"}).find_all(attrs={"class": "dropdown_item"})
    res = []
    for tag in tags:
        link_1 = 'https://bazis-motors.ru' + tag.find("a").get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "inner_wrap TYPE_2"})
        for card in cards:
            link = 'https://bazis-motors.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "item-title"}).find("a").text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            try:
                cost__ = card.find(attrs={"class": "price font-bold font_mxs"}).find("span").text.strip()
            except Exception:
                continue
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


async def tumen_car(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://tumen-car.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brand__item"})
    res = []
    for tag in tags:
        link_1 = 'https://tumen-car.ru' + tag.find("a").get("href")
        time.sleep(0.2)
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card__body"})
        for card in cards:
            link = 'https://tumen-car.ru' + card.find("a").get("href")
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


async def china_tumen(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://china-avto-tumen.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "col-xl-2 col-lg-3 col-md-3 col-6 p-1"})

    res = []
    for tag in tags:
        link_1 = 'https://china-avto-tumen.ru' + tag.find("a").get("href")
        browser.get(link_1)
        time.sleep(2)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "item mb-3"})
        for card in cards:
            link = 'https://china-avto-tumen.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "name mb-3"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "new mr-2"}).text
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


async def autotumen(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autotumen.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brand__item"})
    res = []
    for tag in tags:
        link_1 = 'https://autotumen.ru' + tag.find("a").get("href")
        time.sleep(0.2)
        response = requests.get(link_1, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card__body"})
        for card in cards:
            link = 'https://autotumen.ru' + card.find("a").get("href")
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