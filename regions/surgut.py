import time
import requests
import bs4
import fake_headers

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def autosurgut186(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autosurgut186.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autosurgut186.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def profsouz(dct_up, browser):
    link = 'https://auto-centre-profsouz.ru/auto'
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
        model = title.replace(brand, '').strip().replace(" ", "")
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


# async def aspect(dct_up, browser):
#     link = 'https://aspect-motors.ru/auto'
#     browser.get(link)
#     time.sleep(2)
#     html = browser.page_source
#     soup = bs4.BeautifulSoup(html, 'lxml')
#     cards = soup.find_all(attrs={"class": "main_catalog_item__baselink"})
#     res = []
#     for card in cards:
#         link = card.get("href")
#         title = card.find(attrs={"class": "main_catalog_item__title"}).text.lower().strip()
#         brand = title.split()[0]
#         model = title.replace(brand, '').strip().replace(" ", "")
#         cost__ = card.find(attrs={"class": "main_catalog_item__creditprice"}).text
#         cost_ = ''
#         for y in cost__:
#             if y.isdigit():
#                 cost_ += y
#         cost = int(cost_)
#         name = brand + ', ' + model
#         try:
#             name = dct_up[name]
#         except KeyError:
#             await bot.send_message(CHANEL_ID, f'{name} {link}')
#         res.append([name, cost, link])
#     return res


async def sibir(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://sibir-morots.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://sibir-morots.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def avtosalon_profsouz(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    cnt = 1
    res = []
    while True:
        time.sleep(0.5)
        link = f'https://avtosalon-profsouz.ru/new_auto/page/{cnt}/'
        response = requests.get(link, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "auto-card new_auto"})
        if len(cards) == 0:
            break
        for card in cards:
            link = card.get("href")
            title = card.find(attrs={"class": "auto-card__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
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


async def autocentrsurgut186(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autocentersurgut186.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autocentersurgut186.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def autosalon_hmao(dct_up, browser):
    link = 'https://autosalon-hmao.ru/auto'
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
        model = title.replace(brand, '').strip().replace(" ", "")
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
