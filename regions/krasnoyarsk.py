import time

import requests
import bs4
import fake_headers
from selenium.webdriver.common.by import By

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def carproms_nsk(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://carproms-nsk.ru/catalog'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "flex w-full flex-col px-5 sm:px-7 pb-7 gap-3"})
    res = []
    for card in cards:
        title = 'lada ' + card.find("p").text.lower().strip().replace("(ваз)", "")
        brand = title.split()[0]
        model = title.replace(brand, '').strip().replace(" ", "").replace("|", "i")
        cost__ = card.find(attrs={"class": "flex flex-col gap-1"}).find("div").text
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