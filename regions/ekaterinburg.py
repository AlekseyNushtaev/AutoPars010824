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


async def new_auto_96(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://new-auto96.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://new-auto96.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def auto_196(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://auto-196.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://new-auto96.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def autosalon_kit(dct_up, browser):
    link = 'https://autosalon-kit.ru/auto'
    browser.get(link)
    time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "car-card"})
    res = []
    for card in cards:
        try:
            link = card.find("a").get("href")
            title = card.find("a").text.lower().strip().replace('•', '')
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
        except Exception:
            pass
    return res


async def kit_autoshop(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    cnt = 1
    res = []
    while True:
        time.sleep(0.5)
        link = f'https://kit-autoshop.ru/auto?page={cnt}'
        response = requests.get(link, headers.generate())
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        try:
            cards = soup.find(attrs={"class": "catalog__grid"}).find_all(attrs={"class": "car-card"})
        except Exception:
            break
        if len(cards) == 0:
            break
        for card in cards:
            link = card.find("a").get("href")
            title = card.find(attrs={"class": "car-card__title"}).text.lower().strip()
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
        cnt += 1
    return res


async def primeauto_ekb(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://primeauto-ekb.ru/new'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/section[2]/div/div/button').click()
    except Exception:
        pass
    time.sleep(1)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find_all(attrs={"class": "list__marks-item"})
    res = []
    for tag in tags:
        link_1 = 'https://primeauto-ekb.ru' + tag.find("a").get("href")
        browser.get(link_1)
        time.sleep(1.25)
        time.sleep(0.25)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card--folder--catalog mini-card mini-card--folder"})
        for card in cards:
            link = 'https://primeauto-ekb.ru' + card.get("href")
            brand = card.find(attrs={"class": "mini-card__regular-title"}).text.lower().strip()
            model = card.find(attrs={"class": "mini-card__bold-title"}).text.replace(' ', '').lower().strip()
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


async def atc_gagarin(dct_up):
    link = 'https://atc-gagarin.ru/cars-new/?page=100'
    response = requests.get(link)
    time.sleep(0.5)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "card-body"})
    res = []
    for card in cards:
        link = 'https://atc-gagarin.ru' + card.find("a").get("href")
        title = card.find(attrs={"class": "card-title__title"}).text.lower().strip().replace('(ваз)', '').replace('\xa0', '')
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "")
        cost__ = card.find(attrs={"class": "price-box__current"}).text.strip()
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


async def uu_stocks(dct_up, browser):
    link = 'https://uu-stoks.ru/auto'
    browser.get(link)
    time.sleep(13)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "model"})
    res = []
    for card in cards:
        try:
            link = card.find("a").get("href")
            title = card.find(attrs={"class": "model__name"}).text.lower().replace('автомобиль', '').strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
            costs = card.find_all("div")
            cost__ = ' '
            for cost___ in costs:
                if 'от' in cost___.text:
                    cost__ = cost___.text
                    break
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
        except Exception as e:
            print(e)
    return res


async def autoworld_ekb(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autoworld-ekb.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model pa-3"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autoworld-ekb.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def swmauto_dealer(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://swmauto-dealer.ru/new'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/section/div/button/span').click()
        time.sleep(2)
    except:
        pass
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "popular-marks-list"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://swmauto-dealer.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card mini-card--folder"})
        for card in cards:
            link = 'https://swmauto-dealer.ru' + card.find("a").get("href")
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


async def topautos_ekb(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://topautos-ekb.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://topautos-ekb.ru' + card.find("a").get("href")
        name = dct["brand"].lower().strip() + ', ' + dct["model"].lower().replace(" ", "").strip()
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res
