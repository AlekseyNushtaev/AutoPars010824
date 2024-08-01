import time

import requests
import bs4
import fake_headers
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from pprint import pprint

def autosurgut186():
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
        res.append([dct["brand"].lower() + ', ' + dct["model"].lower(), dct["cost"], link])
    return res


def profsouz():
    chrome_driver_path = ChromeDriverManager().install()
    browser_service = Service(executable_path=chrome_driver_path)
    browser = Chrome(service=browser_service)
    link = 'https://auto-centre-profsouz.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog-item"})
    res = []
    for card in cards:
        link = card.find(attrs={"class": "catalog-item-title"}).get("href")
        brand = link.split("/")[-3]
        model = link.split("/")[-2] + ' ' + link.split("/")[-1]
        cost__ = card.find(attrs={"class": "catalog-item-info__pricing__new"}).text
        cost_ = ''
        for y in cost__:
            if y.isdigit():
                cost_ += y
        cost = int(cost_)
        res.append([brand + ', ' + model, cost, link])
    return res


def aspect():
    chrome_driver_path = ChromeDriverManager().install()
    browser_service = Service(executable_path=chrome_driver_path)
    browser = Chrome(service=browser_service)
    link = 'https://aspect-motors.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "main_catalog_item__baselink"})
    res = []
    for card in cards:
        link = card.get("href")
        title = card.find(attrs={"class": "main_catalog_item__title"}).text.lower().strip()
        brand = title.split()[0]
        model = title.replace(brand, '').strip()
        cost__ = card.find(attrs={"class": "main_catalog_item__creditprice"}).text
        cost_ = ''
        for y in cost__:
            if y.isdigit():
                cost_ += y
        cost = int(cost_)
        res.append([brand + ', ' + model, cost, link])
    return res


def sibir():
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
        res.append([dct["brand"].lower() + ', ' + dct["model"].lower(), dct["cost"], link])
    return res
