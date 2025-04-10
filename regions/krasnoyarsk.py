import time

import requests
import bs4
import fake_headers
from selenium.webdriver.common.by import By

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def car_avangard(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://car-avangard.ru/cars/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "car__list"}).find_all(attrs={"class": "car__item"})
    res = []
    for tag in tags:
        link_1 = 'https://car-avangard.ru' + tag.find("a").get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "car__container"}).find_all(attrs={"class": "card"})
        for card in cards:
            try:
                link = 'https://car-avangard.ru' + card.find("a").get("href")
                title = card.find(attrs={"class": "car__name"}).text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "car__price"}).find("p").text.strip()
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


async def avangard_24(dct_up, browser):
    link = 'https://avangard-24.ru/vehicles'
    browser.get(link)
    time.sleep(5)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "main_catalog_item_content__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "main_catalog_item_content__price"}).text
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


async def lada_krs_m2(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://lada-krs-m2.ru/avto-new/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "mini-card"})
    res = []
    for card in cards:
        link = 'https://lada-krs-m2.ru' + card.get("href")
        title = 'lada ' + card.find(attrs={"class": "mini-card__name"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "mini-card-prices__current"}).text
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


async def lada_kras(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://lada-kras.ru/#models'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "models__item model"})
    res = []
    for card in cards:
        title = 'lada ' + card.find(attrs={"class": "model__title"}).text.lower().strip().replace("(ваз)", "")
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


async def krsk_auto(dct_up, browser):
    link = 'https://krsk-auto.ru/auto'
    browser.get(link)
    time.sleep(5)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "models__item"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "model__img"}).find("a").get("href")
        title = card.find("h3").text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "model__price"}).find("div").text
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


async def krasnoyarsk_carso(dct_up, browser):
    link = 'https://krasnoyarsk.carso.ru/newauto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "crossover-models"})
    res = []
    for tag in tags:
        cards = tag.find_all("a")
        for card in cards:
            link = 'https://krasnoyarsk.carso.ru' + card.get("href")
            title = card.find(attrs={"class": "best-separate__chang"}).text.lower().strip().replace("\n", " ")
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
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


async def autonew_krr(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'http://autonew-krr.ru/avto-new/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brands__card"})
    res = []
    for tag in tags:
        link_1 = 'http://autonew-krr.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card"})
        for card in cards:
            link = 'http://autonew-krr.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "mini-card__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            try:
                cost__ = card.find(attrs={"class": "new text-primary"}).text.strip()
            except:
                cost__ = card.find(attrs={"class": "mini-card__prices"}).find(attrs={"class": "new"}).text.strip()
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


async def sibauto_official(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://sibauto-official.ru/'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div[2]').click()
        time.sleep(2)
    except:
        pass
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "list list__marks"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://sibauto-official.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card mini-card__folder"})
        for card in cards:
            link = 'https://sibauto-official.ru' + card.get("href")
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


async def neokars(dct_up, browser):
    link = 'https://neokars.ru/vehicles'
    browser.get(link)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "main_catalog_item_content__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "main_catalog_item_content__price"}).text
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
