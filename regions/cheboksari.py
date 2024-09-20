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


async def avto_trend(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://avto-trend21.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://avto-trend21.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def avto_shop_21(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://auto-shop-21.ru/catalog'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "brand__item"})
    res = []
    for card in cards:
        link = card.get("href")
        title = card.find(attrs={"class": "brand__item-name"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "brand__item-price-now"}).text
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


async def avto_alyans(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    count = 0
    flag = True
    res_all = []
    while flag:
        time.sleep(0.5)
        link = f'https://alyans-auto.ru/auto/auto.html?curPos={count}'
        count += 40
        response = requests.get(link, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "auto"})
        if len(cards) == 0:
            break
        for card in cards:
            link = 'https://alyans-auto.ru' + card.find("a").get("href")
            title = card.find(attrs={"class": "auto__title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "auto__price"}).text
            cost_ = ''
            for y in cost__:
                if y.isdigit():
                    cost_ += y
            cost = int(cost_)
            name = brand + ', ' + model
            if name == 'киа, lovol':
                continue
            try:
                name = dct_up[name]
            except KeyError:
                await bot.send_message(CHANEL_ID, f'{name} {link}')
            res_all.append([name, cost, link])
    res_dct = {}
    res_name = []
    for item in res_all:
        if item[0] not in res_name:
            res_name.append(item[0])
            res_dct[item[0]] = [item[1], item[2]]
        else:
            if res_dct[item[0]][0] > item[1]:
                res_dct[item[0]] = [item[1], item[2]]
    res = []
    for item in res_dct.keys():
        res.append([item, res_dct[item][0], res_dct[item][1]])
    res.sort()
    return res
