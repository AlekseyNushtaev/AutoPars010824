import time

import requests
import bs4
import fake_headers

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def autonova_nkz(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autonova-nkz.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autonova-nkz.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def autocenter_kemerevo(dct_up, browser):
    link = 'https://autocenter-kemerovo.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source.replace('<br>', ' ')
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "model"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = card.find(attrs={"class": "model__name"}).text.lower().strip()
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


async def autosalon_kemerevo(dct_up, browser):
    link = 'https://autosalon-kemerovo.ru/auto'
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


async def center_carplaza(dct_up, browser):
    link = 'https://center-carplaza.ru/auto'
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


async def carplaza_avtosalon(dct_up):
    cnt = 1
    res = []
    while True:
        link = f'https://carplaza-avtosalon.ru/new_auto/page/{cnt}/'
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


async def carplaza_ac(dct_up):
    cnt = 1
    res = []
    while True:
        link = f'https://carplaza-ac.ru/new_auto/page/{cnt}/'
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


async def car_plaza_42(dct_up, browser):
    link = 'https://car-plaza-42.ru/auto'
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


async def kemerevo_autochina(dct_up):
    cnt = 1
    res = []
    while True:
        link = f'https://kemerovo-autochina.ru/new_auto/page/{cnt}/'
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


async def lada_kemerovo_42(dct_up):
    cnt = 1
    res = []
    while True:
        link = f'https://lada-kemerovo42.ru/new_auto/page/{cnt}/'
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


async def lada_42(dct_up, browser):
    link = 'https://lada-42.ru/'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog-item"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "catalog-item__title"}).get("href")
        title = 'lada ' + card.find(attrs={"class": "catalog-item__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
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


async def auto_atlanta_nkz(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://auto-atlanta-nkz.ru/avto-new/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "brands"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://auto-atlanta-nkz.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card"})
        for card in cards:
            try:
                link = 'https://auto-atlanta-nkz.ru' + card.find("a").get("href")
                title = card.find(attrs={"class": "mini-card__title"}).text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "new text-primary"}).text.strip()
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


async def nkz_autosalon(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://novokuznetsk.autosalon.shop/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "header-brands__list row"}).find_all("a")
    res = []
    for tag in tags[:-1]:
        brand = tag.find(attrs={"class": "header-brands__item-text"}).text.lower().strip()
        link_1 = 'https://novokuznetsk.autosalon.shop' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "models-card__inner"})
        for card in cards:
            try:
                link = 'https://novokuznetsk.autosalon.shop' + card.get("href")
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