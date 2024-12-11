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


def park_auto_sm(dct_up):
        link = 'https://avtosrf5-11.ru/'
        response = requests.get(link)
        time.sleep(0.5)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": "models__item"})
        res = []
        for card in cards:
            link = 'https://avtosrf5-11.ru'
            model = card.find(attrs={"class": "models-item__name h2"}).text.lower().replace(' ', '').strip()
            brand = 'lada'
            cost__ = card.find(attrs={"class": "models-item-info__price"}).text.strip()
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
        return res


#
#
# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
#
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)
# browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
res = park_auto_sm(dct)
print(len(res))
