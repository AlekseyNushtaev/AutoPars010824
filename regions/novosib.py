import time

import requests
import bs4
import fake_headers
from selenium.webdriver.common.by import By

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def carproms_nsk(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://carproms-nsk.ru/catalog'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "flex w-full flex-col px-5 sm:px-7 pb-7 gap-3"})
    res = []
    for card in cards:
        title = 'lada ' + card.find("p").text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "flex flex-col gap-1"}).find("div").text
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


async def lada_novosib(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://lada-novosib.ru/#models'
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


async def sib_autosalon(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://sib-autosalon.ru/cars/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "mark__list"}).find_all(attrs={"class": "mark__link"})
    res = []
    for tag in tags:
        link_1 = 'https://sib-autosalon.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "car-mini__grid"}).find_all(attrs={"class": "car-mini__item"})
        for card in cards:
            link = 'https://sib-autosalon.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "car-mini__name-car"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "car-mini__price-value"}).text.strip()
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


async def ac_azimut(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ac-azimut.ru/new'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/section/div/button').click()
        time.sleep(2)
    except:
        pass
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "popular-marks"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://ac-azimut.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card mini-card--folder"})
        for card in cards:
            link = 'https://ac-azimut.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "mini-card__folder"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "mini-card__price"}).text.strip()
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


async def nsk_drive(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://nsk-drive.ru/new'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/section[2]/div/div/button').click()
        time.sleep(2)
    except:
        pass
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "list__marks"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://nsk-drive.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "catalog__folders"}).find_all("a")
        for card in cards:
            link = 'https://nsk-drive.ru' + card.get("href")
            brand = card.find(attrs={"class": "mini-card__bold-title"}).text.lower().strip()
            model = card.find(attrs={"class": "mini-card__regular-title"}).text.lower().replace(' ', '').strip()
            cost__ = card.find(attrs={"class": "mini-card__prices-price mini-card__prices-price--actual"}).text.strip()
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


async def sibear_auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://sibear-auto.ru/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "brand__list"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://sibear-auto.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card card__main"})
        for card in cards:
            link = 'https://nsk-drive.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "card__special-name"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "card__price-main"}).text.strip()
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


async def nsk_avtomir(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://nsk.avtomir.ru/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "carmodels__item"})
    res = []
    for tag in tags:
        link_1 = 'https://nsk.avtomir.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "card"})
        for card in cards:
            try:
                link = 'https://nsk.avtomir.ru' + card.find("a").get("href")
                title = card.find("a").text.lower().strip()
                brand = title.split()[0]
                model = title.replace(brand, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "card__price-row"}).text.strip()
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


async def centorauto_nsk(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://centorauto-nsk.ru/avto-new/'
    response = requests.get(link, headers.generate())
    time.sleep(0.25)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "brands"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://centorauto-nsk.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card"})
        for card in cards:
            try:
                link = 'https://centorauto-nsk.ru' + card.find("a").get("href")
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


async def kia_novo(dct_up, browser):
    link = 'https://kia-novo.ru/'
    browser.get(link)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item"})
    res = []
    for card in cards:
        link = card.find("a").get("href")
        title = 'kia ' + card.find(attrs={"class": "main_catalog_item__title"}).text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "main_catalog_item__price"}).find("div").text
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