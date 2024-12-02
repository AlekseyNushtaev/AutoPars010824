import asyncio
from datetime import datetime
import shutil


from aiogram import Router, types
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from bot import bot
from config import ADMIN_ID, CHANEL_ID
from json_maker import json_maker
from parser import parser_stavropol, parser_surgut, parser_krasnodar, parser_moscow, parser_volgograd, \
    parser_chelyabinsk, parser_cheboksari, parser_ufa, parser_ekaterinburg, parser_tumen, parser_saratov

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
        options.add_argument("--window-size=1200,600")
        options.add_argument('--disable-dev-shm-usage')
        browser = Chrome(service=browser_service, options=options)
        await parser_stavropol(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/stavropol.xlsx"))
        await parser_saratov(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/saratov.xlsx"))
        await parser_ekaterinburg(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/ekaterinburg.xlsx"))
        await parser_volgograd(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/volgograd.xlsx"))
        await parser_surgut(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/surgut.xlsx"))
        await parser_tumen(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/tumen.xlsx"))
        await parser_cheboksari(dct)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/cheboksari.xlsx"))
        await parser_chelyabinsk(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/chelyabinsk.xlsx"))
        await parser_krasnodar(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/krasnodar.xlsx"))
        await parser_ufa(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/ufa.xlsx"))
        await parser_moscow(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="xlsx/moscow.xlsx"))
        try:
            await json_maker(dct)
        except Exception as e:
            await bot.send_message(ADMIN_ID, f'JSONify error - {str(e)}')
        for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd', 'chelyabinsk',
                       'cheboksari', 'ufa', 'tumen', 'ekaterinburg', 'saratov']:
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
