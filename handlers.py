import asyncio
import time
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
    parser_kazan, parser_kemerovo, parser_omsk, parser_spb, parser_nsk, parser_krsk, parser_himki, parser_toliati, \
    parser_dmitrovka, kemerovo2, toliati2, surgut2, spb2

router = Router()


async def send_doc(chat_id, file):
    while True:
        try:
            await bot.send_document(chat_id, file)
            break
        except:
            time.sleep(1)
            break


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
        if True:
            await spb2(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/spb2.xlsx"))
            await kemerovo2(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/kemerovo2.xlsx"))
            await toliati2(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/toliati2.xlsx"))
            await surgut2(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/surgut2.xlsx"))
            await parser_stavropol(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/stavropol.xlsx"))
            await parser_dmitrovka(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/dmitrovka.xlsx"))
            await parser_himki(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/himki.xlsx"))
            await parser_toliati(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/toliati.xlsx"))
            await parser_samara(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/samara.xlsx"))
            await parser_krsk(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/krsk.xlsx"))
            await parser_nsk(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/nsk.xlsx"))
            await parser_omsk(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/omsk.xlsx"))
            await parser_spb(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/spb.xlsx"))
            await parser_kemerovo(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/kemerovo.xlsx"))
            await parser_saratov(dct)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/saratov.xlsx"))
            await parser_ekaterinburg(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/ekaterinburg.xlsx"))
            await parser_volgograd(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/volgograd.xlsx"))
            await parser_surgut(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/surgut.xlsx"))
            await parser_tumen(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/tumen.xlsx"))
            await parser_cheboksari(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/cheboksari.xlsx"))
            await parser_chelyabinsk(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/chelyabinsk.xlsx"))
            await parser_krasnodar(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/krasnodar.xlsx"))
            await parser_kazan(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/kazan.xlsx"))
            await parser_ufa(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/ufa.xlsx"))
            await parser_moscow(dct, browser)
            await send_doc(CHANEL_ID, types.FSInputFile(path="xlsx/moscow.xlsx"))
        try:
            await json_maker()
        except Exception as e:
            await bot.send_message(ADMIN_ID, f'JSONify error - {str(e)}')
        for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd', 'chelyabinsk', 'kazan', 'spb', 'omsk',
                       'cheboksari', 'ufa', 'tumen', 'ekaterinburg', 'saratov', 'samara', 'kemerovo', 'nsk', 'krsk',
                       'himki', 'toliati', 'dmitrovka', 'kemerovo2', 'toliati2', 'surgut2', 'spb2']:
            shutil.copy(f'csv/{region}.csv', f'/var/www/html/storage/{region}.csv')
            shutil.copy(f'json/{region}.json', f'/var/www/html/storage/{region}.json')
        shutil.copy('models_id.json', '/var/www/html/storage/models_id.json')
        await parser_models()
        shutil.copy('carparser/models.json', '/var/www/html/storage/models.json')
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
