from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import openpyxl
import json
import requests
import bs4
import fake_headers
import time
import unicodedata
import datetime
import os
from pprint import pprint

cars = [
'https://idol-avto.ru/cars-new/jaecoo/j7/2023-allroad-5/',
'https://idol-avto.ru/cars-new/jetour/dashing/2022-allroad-5/',
'https://idol-avto.ru/cars-new/jetour/x70-plus/i-allroad-5/',
'https://idol-avto.ru/cars-new/jetour/x90-plus/2021-allroad-5/']

chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
options.page_load_strategy = 'eager'
options.add_argument("--start-maximized")
browser = Chrome(service=browser_service, options=options)
res = []
for car in cars[:1]:
    dct = {}
    browser.get(car)
    time.sleep(3)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    brand = soup.find_all(attrs={"class": 'breadcrumb'})[2].find("a").text.strip()
    dct['brand'] = brand
    brand_alias = brand.lower().replace(' ', '_')
    dct['brand_alias'] = brand_alias
    model_full = soup.find_all(attrs={"class": 'breadcrumb'})[3].find("a").text.strip()
    model_alias = model_full.lower().replace(' ', '_')
    dct['model_alias'] = model_alias
    dct['model_full'] = model_full
    dct['body'] = 'Кроссовер'
    dct['body_alias'] = 'crossover'
    img = soup.find(attrs={"class": 'image-box__image'}).get('src')
    dct['img_url'] = img
    colors = []
    cols = soup.find(attrs={"class": 'select__color-list'}).find_all("button")
    for col in cols:
        dct_1 = {}
        name = col.get("aria-label")
        dct_1['name'] = name
        img_url = col.get("style").replace("background-image:url('", "")[:-3]
        dct_1['color_hex'] = '#000000'
        dct_1['color_hex_2'] = '#000000'
        dct_1['img_url'] = img_url
        colors.append(dct_1)
    dct['colors'] = colors
    galleries = []
    imgs = soup.find(attrs={"class": 'media-bock__images'}).find_all("img")
    number = 1
    for img in imgs:
        dct_2 = {}
        img_url = img.get("src")
        dct_2['url'] = img_url
        dct_2['type'] = 'exterior'
        dct_2['sort_order'] = number
        number += 1
        galleries.append(dct_2)
    dct['galleries'] = galleries

    prices = []

    tags = soup.find(attrs={"class": 'modification-list'}).find_all(
        attrs={"class": 'main-link accordion-content__link'})
    for tag in tags:
        dct_3 = {}
        browser.get('https://idol-avto.ru' + tag.get("href"))
        time.sleep(3)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        dct_3['body'] = 'Кроссовер'
        complectation = soup.find(attrs={"class": 'accordion-trigger__title'}).text.strip()
        dct_3['complectation'] = complectation
        complectation_alias =complectation.lower().replace(" ", "_")
        dct_3['complectation_alias'] = complectation_alias
        dct_3['doors'] = 5
        cost_ = soup.find(attrs={"class": 'buy__base-price _base-price'}).text.strip()
        cost = ''
        for p in cost_:
            if p.isdigit():
                cost += p
        dct_3['cost'] = int(cost)
        cost_discount_ = soup.find(attrs={"class": 'buy__price'}).text.strip()
        cost_discount = ''
        for p in cost_discount_:
            if p.isdigit():
                cost_discount += p
        dct_3['cost_discount'] = int(cost_discount)
        engine_type = soup.find(attrs={"class": 'tech-detail__value'}).text.strip()
        dct_3['engine_type'] = engine_type
        techs = soup.find(attrs={"class": 'tabs__content'}).find_all(attrs={"class": 'row'})
        for tech in techs:
            name = tech.find(attrs={"class": 'row__title'}).text.strip()
            value = tech.find(attrs={"class": 'cell'}).text.strip()
            if name == 'Объем':
                dct_3['engine_volume'] = int(value)
            if name == 'Мощность кВт.':
                dct_3['engine_power'] = int(value)
            if name == 'Максимальный крутящий момент':
                torque = value
            if name == 'Обороты максимального крутящего момента':
                torque_value = value.split(',')[1].strip()
            if name == 'Марка топлива':
                dct_3['fuel'] = 'Бензин ' + value
            if name == 'Трансмиссия':
                dct_3['gearbox'] = value
                if value == 'Механика':
                    dct_3['gearbox_auto'] = 0
                if value == 'Робот':
                    dct_3['gearbox_auto'] = 1
            if name == 'Кол-во передач':
                dct_3['gears'] = int(value)
            if name == 'Привод':
                dct_3['transmission'] = value
            if name == 'Клиренс':
                dct_3['clearence'] = value
            if name == 'Колёсная база':
                dct_3['dim_base'] = value






        prices.append(dct_3)
    dct['prices'] = prices


    res.append(dct)
pprint(res)