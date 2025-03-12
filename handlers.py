import asyncio
from datetime import datetime
import shutil


from aiogram import Router, types
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from bot import bot
from carparser.parser_models import parser_models
from config import ADMIN_ID, CHANEL_ID
from json_maker import json_maker
from parser import parser_stavropol, parser_surgut, parser_krasnodar, parser_moscow, parser_volgograd, \
    parser_chelyabinsk, parser_cheboksari, parser_ufa, parser_ekaterinburg, parser_tumen, parser_saratov, parser_samara, \
    parser_yaroslavl, parser_novokuzneck, parser_kazan

router =Router()


async def pars():
    try:
        dct = {}
        shutil.copy('id.xlsx', '/var/www/html/storage/id.xlsx')
        with open('autolist.txt', 'r', encoding='utf-8') as f:
            lst = f.readlines()
            for item in lst:
                dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
        chrome_driver_path = ChromeDriverManager().install()
        browser_service = Service(executable_path=chrome_driver_path)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser = Chrome(service=browser_service, options=options)
        browser.maximize_window()
        print(1)
        await parser_stavropol(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/stavropol.xlsx"))
        print(2)
        await parser_samara(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/samara.xlsx"))
        print(3)
        await parser_yaroslavl(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/yaroslavl.xlsx"))
        print(4)
        await parser_novokuzneck(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/novokuzneck.xlsx"))
        print(5)
        await parser_saratov(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/saratov.xlsx"))
        print(6)
        await parser_ekaterinburg(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/ekaterinburg.xlsx"))
        print(7)
        await parser_volgograd(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/volgograd.xlsx"))
        print(8)
        await parser_surgut(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/surgut.xlsx"))
        print(9)
        await parser_tumen(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/tumen.xlsx"))
        print(10)
        await parser_cheboksari(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/cheboksari.xlsx"))
        print(11)
        await parser_chelyabinsk(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/chelyabinsk.xlsx"))
        print(12)
        await parser_krasnodar(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/krasnodar.xlsx"))
        print(13)
        await parser_kazan(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/kazan.xlsx"))
        print(14)
        await parser_ufa(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/ufa.xlsx"))
        await parser_moscow(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/moscow.xlsx"))
        await parser_models()
        shutil.copy('carparser/models.json', '/var/www/html/storage/models.json')
        try:
            await json_maker(dct)
        except Exception as e:
            await bot.send_message(ADMIN_ID, f'JSONify error - {str(e)}')
        for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd', 'chelyabinsk', 'kazan',
                       'cheboksari', 'ufa', 'tumen', 'ekaterinburg', 'saratov', 'samara', 'yaroslavl', 'novokuzneck']:
            shutil.copy(f'csv/{region}.csv', f'/var/www/html/storage/{region}.csv')
            shutil.copy(f'json/{region}.json', f'/var/www/html/storage/{region}.json')
        browser.quit()
    except Exception as e:
        await bot.send_message(ADMIN_ID, str(e))


async def scheduler():
    await pars()
    while True:
        time = datetime.now()
        if str(time.hour) == '7':
            await pars()
            await asyncio.sleep(3600)
        await asyncio.sleep(60)
