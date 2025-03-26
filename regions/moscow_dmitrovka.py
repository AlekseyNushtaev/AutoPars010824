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


async def fili_auto(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://fili-auto.ru/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "brand__list"}).find_all(attrs={"class": "brand__item"})
    res = []
    for br in brands:
        brand_link = 'https://fili-auto.ru' + br.find("a").get("href")
        response = requests.get(brand_link, headers.generate())
        time.sleep(0.2)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find(attrs={"class": "car__catalog"}).find_all(attrs={"class": "card__body"})
        for card in cards:
            link = 'https://fili-auto.ru' + card.find("a").get("href")
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


async def plusauto_moscow(dct_up, browser):
    link = 'https://plusauto.moscow/'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    brands = soup.find(attrs={"class": "brands"}).find_all(attrs={"class": "brand-item"})
    res = []
    for br in brands:
        try:
            brand_link = br.find("a").get("href")
            brand = br.find("a").get("title").lower().strip()
            browser.get(brand_link)
            time.sleep(1)
            time.sleep(0.25)
            html = browser.page_source
            soup = bs4.BeautifulSoup(html, 'lxml')
            cards = soup.find(attrs={"class": "model-cards"}).find_all(attrs={"class": "model-card"})
            for card in cards:
                try:
                    link = card.find("a").get("href")
                    model = card.find(attrs={"class": "title"}).text.lower().strip().replace(" ", "")
                    cost__ = card.find(attrs={"class": "price"}).text
                    cost_ = ''
                    for y in cost__:
                        if y.isdigit():
                            cost_ += y
                    name = brand + ', ' + model
                    cost = int(cost_)
                    try:
                        name = dct_up[name]
                    except KeyError:
                        await bot.send_message(CHANEL_ID, f'{name} {link}')
                    res.append([name, cost, link])
                except:
                    pass
        except AttributeError:
            pass
    return res
