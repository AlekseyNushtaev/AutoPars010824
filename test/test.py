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


def l_auto(dct_up, browser):
    link = 'https://l-auto16.ru/catalog/'
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
        link = 'https://l-auto16.ru' + card.get("href")
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
            print(name, link)
        res.append([name, price, link])
    return res




chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1200,600")

options.add_argument('--disable-dev-shm-usage')
browser = Chrome(service=browser_service, options=options)
browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = l_auto(dct, browser)
print(len(res))
