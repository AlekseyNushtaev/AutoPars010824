import asyncio
from datetime import datetime


from aiogram import Router, types
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from bot import bot
from config import ADMIN_ID, CHANEL_ID
from parser import parser_stavropol, parser_surgut, parser_krasnodar, parser_moscow

router =Router()


async def pars():
    try:
        dct = {}
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
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="stavropol.xlsx"))
        await parser_surgut(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="surgut.xlsx"))
        await parser_krasnodar(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="krasnodar.xlsx"))
        await parser_moscow(dct, browser)
        await bot.send_document(CHANEL_ID, types.FSInputFile(path="moscow.xlsx"))
        browser.quit()
    except Exception as e:
        await bot.send_message(ADMIN_ID, str(e))
async def scheduler():
    await pars()
    while True:
        time = datetime.now()
        if str(time.hour) == '10':
            await pars()
            await asyncio.sleep(3600)
        await asyncio.sleep(60)


