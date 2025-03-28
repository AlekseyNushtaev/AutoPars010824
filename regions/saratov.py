import asyncio
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
                await asyncio.sleep(0.1)
            res.append([name, cost, link])
    return res


async def autocenter_saratov(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autocenter-saratov.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autocenter-saratov.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
            await asyncio.sleep(0.1)
        res.append([name, dct["cost"], link])
    return res


async def cartrade_saratov(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://cartrade-saratov.ru/auto'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "car-card__pricing-main"}).text
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
            await asyncio.sleep(0.1)
        res.append([name, cost, link])
    return res


async def autodealer_saratov(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    cnt = 1
    res = []
    while True:
        time.sleep(0.5)
        link = f'https://autodealer-saratov.ru/auto?page={cnt}'
        response = requests.get(link, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        try:
            cards = soup.find(attrs={"class": "catalog__grid"}).find_all(attrs={"class": "car-card"})
        except Exception:
            break
        if len(cards) == 0:
            break
        for card in cards:
            link = card.find("a").get("href")
            title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "car-card__price-value"}).text
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
                await asyncio.sleep(0.1)
            res.append([name, cost, link])
        cnt += 1
    return res


async def automarket_saratov(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://automarket-saratov.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://automarket-saratov.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
            await asyncio.sleep(0.1)
        res.append([name, dct["cost"], link])
    return res


async def saratov_autosalon(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov.avtosalon.shop/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "header-brands__list row"}).find_all("a")
    res = []
    for tag in tags:
        brand = tag.find(attrs={"class": "header-brands__item-text"}).text.lower().strip()
        link_1 = 'https://saratov.autosalon.shop' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "models-card__inner"})
        for card in cards:
            try:
                link = 'https://saratov.autosalon.shop' + card.get("href")
                model = card.find(attrs={"class": "models-card__name"}).text.lower().strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "models-card__price-new"}).text.strip()
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


async def saratov_asavtomotors(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov.asavtomotors.ru/catalog/cars/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "CatalogSectionItem"})
    res = []
    for card in cards:
        link = 'https://saratov.asavtomotors.ru' + card.find("a").get("href")
        title = card.find(attrs={"class": "CatalogSectionItem_Name"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "CatalogSectionItem_Price"}).text
        cost_ = ''
        for y in cost__:
            if y.isdigit():
                cost_ += y
        cost = int(cost_)
        name = brand + ', ' + model
        try:
            name = dct_up[name]
        except:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, cost, link])
    return res


async def saratov_autospot(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saratov.autospot.ru/brands/'
    response = requests.get(link, headers.generate())
    time.sleep(0.5)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"data-testid": "allBrands-block"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://saratov.autospot.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.5)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "brand-model-catalog"}).find_all(attrs={"class": "brand-model-card"})
        for card in cards:
            link = 'https://saratov.autospot.ru' + card.find("a").get("href")
            title = card.find("a").text.replace(' • ', ' ').lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            try:
                cost__ = card.find(attrs={"class": "brand-model-card__price-sale"}).text.strip()
            except:
                cost__ = card.find(attrs={"class": "brand-model-card__price"}).text.strip()
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
            except:
                await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
    return res
