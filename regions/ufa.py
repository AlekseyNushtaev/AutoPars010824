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


async def avto_rb(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://avtolininiya-rb.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://avtolininiya-rb.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def ufa_masmotors(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ufa.masmotors.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "region region-sidebar-first"}).find_all("li")
    res = []
    for tag in tags:
        link_1 = 'https://ufa.masmotors.ru' + tag.find("a").get("href")
        browser.get(link_1)
        time.sleep(1)
        time.sleep(0.25)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "brnd_model js-save-storage"})
        for card in cards:
            link = 'https://ufa.masmotors.ru' + card.get("data-href")
            brand = card.get("data-brand").lower().strip()
            model = card.get("data-model").lower().strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "model_price"}).text.strip()
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


async def avrora(dct_up, browser):
    link = 'https://avrora-motors.ru/catalog'
    browser.get(link)
    time.sleep(2)
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://avrora-motors.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip().replace("š", "s").replace('\xa0', '')
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "car-card__price"}).text
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


async def ufa_autospot(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ufa.autospot.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brand-list__item menu-model-navigation-item js-auto-popover-reference-point-container"})
    res = []
    for tag in tags:
        link_1 = 'https://ufa.autospot.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "brand-model-card"})
        for card in cards:
            link = 'https://ufa.autospot.ru' + card.find("a").get("href")
            title = card.find("a").text.lower().strip().replace('•', '')
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            try:
                cost__ = card.find(attrs={"class": "brand-model-card__price-sale"}).text.strip()
            except Exception:
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
            except KeyError:
                await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
    return res


async def alpha_tank(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://alfa-tank.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-info col"})
    res = []
    for card in cards:
        try:
            link = 'https://alfa-tank.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "text-white h2"}).text.lower().strip().replace('•', '')
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "q-ml-sm"}).text.strip()
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
        except Exception:
            pass
    return res


async def ufa_autofort(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autofort-ufa.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "brands__card"})
    res = []
    for tag in tags:
        link_1 = 'https://autofort-ufa.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card"})
        for card in cards:
            link = 'https://autofort-ufa.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "mini-card__title mb-1"}).text.lower().strip()
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
    return res


async def motors_ag(dct_up, browser):
    link = 'https://motors-ag.ru/'
    browser.get(link)
    time.sleep(2)
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        link = 'https://motors-ag.ru' + card.get("href")
        title = card.find(attrs={"class": "car-card__title"}).text.lower().strip().replace('š', 's').replace('\xa0', '')
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "car-card__price"}).text.strip()
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


async def alga_auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://alga-auto.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://alga-auto.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res
