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


async def ac_aquamarine(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ac-aquamarine.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://ac-aquamarine.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def smolino_motors(dct_up, browser):
    link = 'https://smolino-motors74.ru/catalog'
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
        link = 'https://smolino-motors74.ru' + card.get("href")
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


async def che_motors(dct_up, browser):
    link = 'https://che-motors-2024.ru/catalog'
    browser.get(link)
    time.sleep(2)
    SCROLL_PAUSE_TIME = 1

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
    cards = soup.find_all(attrs={"class": "UiLink_UiLink__pbmRv UiLink CatalogCar_CatalogCar__6ku6m"})
    res = []
    for card in cards:
        link = 'https://che-motors-2024.ru' + card.get("href")
        title = card.find(attrs={"class": "CatalogCar_CatalogCarTitle__sqMzF"}).text.lower().strip().replace("š", "s")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "CatalogCar_CatalogCarPrice__2905b"}).text
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


async def saturn2(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://saturn2.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "nav__item"}).find_all(attrs={"class": "nav__item-drop"})
    res = []
    for brand in brands:
        link = 'https://saturn2.ru' + brand.find("a").get("href")
        browser.get(link)
        time.sleep(10)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "post-wrapper__grid"}).find_all(attrs={"class": "post-preview"})
        for card in cards:
            try:
                link = 'https://saturn2.ru' + card.find("a").get("href")
                title = card.find(attrs={"class": "post-preview__row"}).find(attrs={"class": "post-preview__name"}).text.lower().strip().replace(",", "")
                marka = title.split()[0]
                model = title.replace(marka, '').strip().replace(" ", "")
                cost__ = card.find(attrs={"class": "post-preview__price"}).text
                cost_ = ''
                for y in cost__:
                    if y.isdigit():
                        cost_ += y
                cost = int(cost_)
                name = marka + ', ' + model
                try:
                    name = dct_up[name]
                except KeyError:
                    await bot.send_message(CHANEL_ID, f'{name} {link}')
                res.append([name, cost, link])
            except Exception:
                continue
    return res


async def avto_mg(dct_up, browser):
    link = 'https://avto-mg.ru/catalog'
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
        link = 'https://avto-mg.ru' + card.get("href")
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


async def avto_zlt(dct_up, browser):
    link = 'https://avto-zlt.ru/'
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
        link = 'https://avto-zlt.ru' + card.get("href")
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


async def avto_graf(dct_up, browser):
    link = 'https://avto-graf-newcars.ru/catalog'
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
    cards = soup.find_all(attrs={"class": "UiLink_UiLink__pbmRv UiLink CatalogCar_CatalogCar__6ku6m"})
    res = []
    for card in cards:
        link = 'https://avto-graf-newcars.ru' + card.get("href")
        title = card.find(attrs={"class": "CatalogCar_CatalogCarTitle__sqMzF"}).text.lower().strip().replace('\xa0', '').replace("š", "s")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "CatalogCar_CatalogCarPrice__2905b"}).text
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


async def ac_174auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://ac-174auto.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://ac-174auto.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def kc_klassavto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://kc-klassavto.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://kc-klassavto.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def carsklad_174(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://carsklad-174.ru/auto'
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
        res.append([name, cost, link])
    return res


async def mnogo_auto_174(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://mnogo-auto174.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://kc-klassavto.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])

    return res


async def kcelitauto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://kcelitauto.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://kcelitauto.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def auto_graf74(dct_up, browser):
    link = 'https://auto-graf74.ru/catalog'
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
        link = 'https://auto-graf74.ru' + card.get("href")
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
