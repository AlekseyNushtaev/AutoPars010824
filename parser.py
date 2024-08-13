import csv

import openpyxl
from bot import bot
from config import ADMIN_ID, CHANEL_ID
from regions.stavropol import autoshop26
from regions.surgut import *
from regions.krasnodar import *
from regions.moscow import *


async def parser_stavropol(dct_up):
    try:
        res = await autoshop26(dct_up)
    except Exception as e:
        res = []
        await bot.send_message(CHANEL_ID, 'https://autoshop26.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    res.sort(key=lambda x: x[0])
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    dct_id = {}
    with open('autolist.txt', 'r', encoding='utf-8') as f:
        lst = f.readlines()
    for item in lst:
        try:
            dct_id[item.split('|')[1].strip()] = item.split('|')[2].strip()
        except Exception:
            pass
    sheet.cell(row=1, column=1).value = 'id'
    sheet.cell(row=1, column=2).value = 'brand'
    sheet.cell(row=1, column=3).value = 'model'
    sheet.cell(row=1, column=4).value = 'min_price'
    sheet.cell(row=1, column=5).value = 'min_price_url'
    sheet.cell(row=1, column=6).value = 'autoshop26.ru'
    sheet.cell(row=1, column=7).value = 'autoshop26.ru_price'
    for i in range(2, len(res) + 2):
        sheet.cell(row=i, column=1).value = dct_id[res[i - 2][0].strip()]
        sheet.cell(row=i, column=2).value = res[i - 2][0].split(', ')[0]
        sheet.cell(row=i, column=2).value = res[i-2][0].split(', ')[0]
        sheet.cell(row=i, column=3).value = res[i-2][0].split(', ')[1]
        sheet.cell(row=i, column=4).value = res[i-2][1]
        sheet.cell(row=i, column=5).value = res[i-2][2]
        sheet.cell(row=i, column=6).value = res[i-2][1]
        sheet.cell(row=i, column=7).value = res[i-2][2]
    wb.save('xlsx/stavropol.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/stavropol.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_krasnodar(dct_up, browser):
    try:
        res_1 = await krd_93_auto(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://krd93-auto.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await car_kranodar(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://car-krasnodar.ru/cars/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await avangard_yug(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://avangard-yug.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await ac_pegas(dct_up,browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://ac-pegas.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await rostov_avto(dct_up, browser)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://rostov-avto-1.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_6 = await loft_autoug(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://loft-autoug.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
    res_6_name = [x[0] for x in res_6]
    res_name = []
    for item in res:
        if item[0] not in res_name:
            res_name.append(item[0])
    res_name.sort()
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    dct_id = {}
    with open('autolist.txt', 'r', encoding='utf-8') as f:
        lst = f.readlines()
    for item in lst:
        try:
            dct_id[item.split('|')[1].strip()] = item.split('|')[2].strip()
        except Exception:
            pass
    sheet.cell(row=1, column=1).value = 'id'
    sheet.cell(row=1, column=2).value = 'brand'
    sheet.cell(row=1, column=3).value = 'model'
    sheet.cell(row=1, column=4).value = 'min_price'
    sheet.cell(row=1, column=5).value = 'min_price_url'
    sheet.cell(row=1, column=6).value = 'krd93-auto.ru'
    sheet.cell(row=1, column=7).value = 'krd93-auto.ru_price'
    sheet.cell(row=1, column=8).value = 'car-krasnodar.ru'
    sheet.cell(row=1, column=9).value = 'car-krasnodar.ru_price'
    sheet.cell(row=1, column=10).value = 'avangard-yug.ru'
    sheet.cell(row=1, column=11).value = 'avangard-yug.ru_price'
    sheet.cell(row=1, column=12).value = 'ac-pegas.ru'
    sheet.cell(row=1, column=13).value = 'ac-pegas.ru_price'
    sheet.cell(row=1, column=14).value = 'rostov-avto-1.ru'
    sheet.cell(row=1, column=15).value = 'rostov-avto-1.ru_price'
    sheet.cell(row=1, column=16).value = 'loft-autoug.ru'
    sheet.cell(row=1, column=17).value = 'loft-autoug.ru_price'

    for i in range(2, len(res_name) + 2):
        sheet.cell(row=i, column=1).value = dct_id[res[i - 2][0].strip()]
        sheet.cell(row=i, column=2).value = res_name[i-2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i-2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i-2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i-2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=8).value = res_2[index][1]
            sheet.cell(row=i, column=9).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        if res_name[i-2] in res_3_name:
            index = res_3_name.index(res_name[i - 2])
            sheet.cell(row=i, column=10).value = res_3[index][1]
            sheet.cell(row=i, column=11).value = res_3[index][2]
            dct[str(res_3[index][1])] = res_3[index][2]
            lst.append(int(res_3[index][1]))
        if res_name[i-2] in res_4_name:
            index = res_4_name.index(res_name[i - 2])
            sheet.cell(row=i, column=12).value = res_4[index][1]
            sheet.cell(row=i, column=13).value = res_4[index][2]
            dct[str(res_4[index][1])] = res_4[index][2]
            lst.append(int(res_4[index][1]))
        if res_name[i-2] in res_5_name:
            index = res_5_name.index(res_name[i - 2])
            sheet.cell(row=i, column=14).value = res_5[index][1]
            sheet.cell(row=i, column=15).value = res_5[index][2]
            dct[str(res_5[index][1])] = res_5[index][2]
            lst.append(int(res_5[index][1]))
        if res_name[i-2] in res_6_name:
            index = res_6_name.index(res_name[i - 2])
            sheet.cell(row=i, column=16).value = res_6[index][1]
            sheet.cell(row=i, column=17).value = res_6[index][2]
            dct[str(res_6[index][1])] = res_6[index][2]
            lst.append(int(res_6[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/krasnodar.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/krasnodar.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_surgut(dct_up, browser):
    try:
        res_1 = await autosurgut186(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://autosurgut186.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await profsouz(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://auto-centre-profsouz.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await aspect(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://aspect-motors.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await sibir(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://sibir-morots.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_name = []
    for item in res:
        if item[0] not in res_name:
            res_name.append(item[0])
    res_name.sort()
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    dct_id = {}
    with open('autolist.txt', 'r', encoding='utf-8') as f:
        lst = f.readlines()
    for item in lst:
        try:
            dct_id[item.split('|')[1].strip()] = item.split('|')[2].strip()
        except Exception:
            pass
    sheet.cell(row=1, column=1).value = 'id'
    sheet.cell(row=1, column=2).value = 'brand'
    sheet.cell(row=1, column=3).value = 'model'
    sheet.cell(row=1, column=4).value = 'min_price'
    sheet.cell(row=1, column=5).value = 'min_price_url'
    sheet.cell(row=1, column=6).value = 'autosurgut186.ru'
    sheet.cell(row=1, column=7).value = 'autosurgut186.ru_price'
    sheet.cell(row=1, column=8).value = 'auto-centre-profsouz.ru'
    sheet.cell(row=1, column=9).value = 'auto-centre-profsouz.ru_price'
    sheet.cell(row=1, column=10).value = 'aspect-motors.ru'
    sheet.cell(row=1, column=11).value = 'aspect-motors.ru_price'
    sheet.cell(row=1, column=12).value = 'sibir-morots.ru'
    sheet.cell(row=1, column=13).value = 'sibir-morots.ru_price'

    for i in range(2, len(res_name) + 2):
        sheet.cell(row=i, column=1).value = dct_id[res[i - 2][0].strip()]
        sheet.cell(row=i, column=2).value = res_name[i-2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i-2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i-2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i-2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=8).value = res_2[index][1]
            sheet.cell(row=i, column=9).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        if res_name[i-2] in res_3_name:
            index = res_3_name.index(res_name[i - 2])
            sheet.cell(row=i, column=10).value = res_3[index][1]
            sheet.cell(row=i, column=11).value = res_3[index][2]
            dct[str(res_3[index][1])] = res_3[index][2]
            lst.append(int(res_3[index][1]))
        if res_name[i-2] in res_4_name:
            index = res_4_name.index(res_name[i - 2])
            sheet.cell(row=i, column=12).value = res_4[index][1]
            sheet.cell(row=i, column=13).value = res_4[index][2]
            dct[str(res_4[index][1])] = res_4[index][2]
            lst.append(int(res_4[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/surgut.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/surgut.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_moscow(dct_up, browser):
    try:
        await bot.send_message(ADMIN_ID, 'begin https://nord-car.ru/catalog')
        res_1 = await nord_car(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://nord-car.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://dc-dbr.ru/catalog')
        res_2 = await dc_dbr(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://dc-dbr.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://autos-s.ru/auto')
        res_3 = await autos_s(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://autos-s.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://warshauto.ru/')
        res_4 = await warshauto(dct_up, browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://warshauto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://kosmos-cars.ru/')
        res_5 = await kosmos_cars(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://kosmos-cars.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://idol-avto.ru/cars-new/?page=100')
        res_6 = await idol_avto(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://idol-avto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://vita-auto.ru/')
        res_7 = await vita_avto(dct_up)
    except Exception as e:
        res_7 = []
        await bot.send_message(CHANEL_ID, 'https://vita-auto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://alcon-auto.ru')
        res_8 = await alcon_avto(dct_up, browser)
    except Exception as e:
        res_8 = []
        await bot.send_message(CHANEL_ID, 'https://alcon-auto.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
    res_6_name = [x[0] for x in res_6]
    res_7_name = [x[0] for x in res_7]
    res_8_name = [x[0] for x in res_8]
    res_name = []
    for item in res:
        if item[0] not in res_name:
            res_name.append(item[0])
    res_name.sort()
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    dct_id = {}
    with open('autolist.txt', 'r', encoding='utf-8') as f:
        lst = f.readlines()
    for item in lst:
        try:
            dct_id[item.split('|')[1].strip()] = item.split('|')[2].strip()
        except Exception:
            pass
    sheet.cell(row=1, column=1).value = 'id'
    sheet.cell(row=1, column=2).value = 'brand'
    sheet.cell(row=1, column=3).value = 'model'
    sheet.cell(row=1, column=4).value = 'min_price'
    sheet.cell(row=1, column=5).value = 'min_price_url'
    sheet.cell(row=1, column=6).value = 'nord-car.ru'
    sheet.cell(row=1, column=7).value = 'nord-car.ru_price'
    sheet.cell(row=1, column=8).value = 'dc-dbr.ru'
    sheet.cell(row=1, column=9).value = 'dc-dbr.ru_price'
    sheet.cell(row=1, column=10).value = 'autos-s.ru'
    sheet.cell(row=1, column=11).value = 'autos-s.ru_price'
    sheet.cell(row=1, column=12).value = 'warshauto.ru'
    sheet.cell(row=1, column=13).value = 'warshauto.ru_price'
    sheet.cell(row=1, column=14).value = 'kosmos-cars.ru'
    sheet.cell(row=1, column=15).value = 'kosmos-cars.ru_price'
    sheet.cell(row=1, column=16).value = 'idol-avto.ru'
    sheet.cell(row=1, column=17).value = 'idol-avto.ru_price'
    sheet.cell(row=1, column=18).value = 'vita-auto.ru'
    sheet.cell(row=1, column=19).value = 'vita-auto.ru_price'
    sheet.cell(row=1, column=20).value = 'alcon-auto.ru'
    sheet.cell(row=1, column=21).value = 'alcon-auto.ru_price'

    for i in range(2, len(res_name) + 2):
        sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        sheet.cell(row=i, column=2).value = res_name[i-2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i-2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i-2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i-2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=8).value = res_2[index][1]
            sheet.cell(row=i, column=9).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        if res_name[i-2] in res_3_name:
            index = res_3_name.index(res_name[i - 2])
            sheet.cell(row=i, column=10).value = res_3[index][1]
            sheet.cell(row=i, column=11).value = res_3[index][2]
            dct[str(res_3[index][1])] = res_3[index][2]
            lst.append(int(res_3[index][1]))
        if res_name[i-2] in res_4_name:
            index = res_4_name.index(res_name[i - 2])
            sheet.cell(row=i, column=12).value = res_4[index][1]
            sheet.cell(row=i, column=13).value = res_4[index][2]
            dct[str(res_4[index][1])] = res_4[index][2]
            lst.append(int(res_4[index][1]))
        if res_name[i-2] in res_5_name:
            index = res_5_name.index(res_name[i - 2])
            sheet.cell(row=i, column=14).value = res_5[index][1]
            sheet.cell(row=i, column=15).value = res_5[index][2]
            dct[str(res_5[index][1])] = res_5[index][2]
            lst.append(int(res_5[index][1]))
        if res_name[i-2] in res_6_name:
            index = res_6_name.index(res_name[i - 2])
            sheet.cell(row=i, column=16).value = res_6[index][1]
            sheet.cell(row=i, column=17).value = res_6[index][2]
            dct[str(res_6[index][1])] = res_6[index][2]
            lst.append(int(res_6[index][1]))
        if res_name[i-2] in res_7_name:
            index = res_7_name.index(res_name[i - 2])
            sheet.cell(row=i, column=18).value = res_7[index][1]
            sheet.cell(row=i, column=19).value = res_7[index][2]
            dct[str(res_7[index][1])] = res_7[index][2]
            lst.append(int(res_7[index][1]))
        if res_name[i-2] in res_8_name:
            index = res_8_name.index(res_name[i - 2])
            sheet.cell(row=i, column=20).value = res_8[index][1]
            sheet.cell(row=i, column=21).value = res_8[index][2]
            dct[str(res_8[index][1])] = res_8[index][2]
            lst.append(int(res_8[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/moscow.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/moscow.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)