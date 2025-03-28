import csv
import json
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



def tumen_salon(dct_up, browser):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://tumen-salon.ru'
    browser.get(link)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div[2]').click()
        time.sleep(2)
    except:
        browser.find_element(By.XPATH, '/html/body/div/div[2]/div/a').click()
        time.sleep(2)
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div[2]').click()
        time.sleep(2)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    tags = soup.find(attrs={"class": "list__marks--full list list__marks"}).find_all("a")
    res = []
    for tag in tags:
        link_1 = 'https://tumen-salon.ru' + tag.get("href")
        response = requests.get(link_1, headers.generate())
        time.sleep(0.25)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "mini-card mini-card__folder"})
        for card in cards:
            link = 'https://tumen-salon.ru' + card.get("href")
            title = card.find(attrs={"class": "mini-card__folder-title"}).text.lower().strip()
            brand = title.split()[0]
            model = title.replace(brand, '').strip().replace(" ", "")
            cost__ = card.find(attrs={"class": "mini-card__folder-prices"}).text.strip()
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
                pass
                # await bot.send_message(CHANEL_ID, f'{name} {link}')
            res.append([name, cost, link])
            print([name, cost, link])
    return res


chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument("--window-size=1200,600")

options.add_argument('--disable-dev-shm-usage')
browser = Chrome(service=browser_service, options=options)
browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = tumen_salon(dct, browser)
print(len(res))
