import csv

import openpyxl
from bot import bot
from config import ADMIN_ID, CHANEL_ID
from regions.stavropol import *
from regions.volgograd import *
from regions.surgut import *
from regions.krasnodar import *
from regions.moscow import *
from regions.chelyabinsk import *
from regions.cheboksari import *
from regions.ufa import *
from regions.ekaterinburg import *
from regions.tumen import *
from pprint import pprint


async def parser_ekaterinburg(dct_up):
    try:
        res_1 = await new_auto_96(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://new-auto96.ru/auto/')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1
    res_1_name = [x[0] for x in res_1]
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
    sheet.cell(row=1, column=6).value = 'new-auto96.ru'
    sheet.cell(row=1, column=7).value = 'new-auto96.ru_price'
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i - 2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/ekaterinburg.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/ekaterinburg.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_volgograd(dct_up, browser):
    try:
        res_1 = await vlg_autotrade(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://vlg-autotrade.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await vlg_autostore(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://volgograd-autostore.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
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
    sheet.cell(row=1, column=6).value = 'vlg-autotrade.ru'
    sheet.cell(row=1, column=7).value = 'vlg-autotrade.ru_price'
    sheet.cell(row=1, column=8).value = 'volgograd-autostore.ru'
    sheet.cell(row=1, column=9).value = 'volgograd-autostore.ru'
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i - 2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i - 2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=8).value = res_2[index][1]
            sheet.cell(row=i, column=9).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/volgograd.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/volgograd.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_stavropol(dct_up):
    try:
        res_1 = await autoshop26(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://autoshop26.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await autocenter_stav(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://autocenter-stav.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
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
    sheet.cell(row=1, column=6).value = 'autoshop26.ru'
    sheet.cell(row=1, column=7).value = 'autoshop26.ru_price'
    sheet.cell(row=1, column=8).value = 'autocenter-stav.ru'
    sheet.cell(row=1, column=9).value = 'autocenter-stav.ru_price'
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i - 2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=6).value = res_1[index][1]
            sheet.cell(row=i, column=7).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i - 2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=8).value = res_2[index][1]
            sheet.cell(row=i, column=9).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/stavropol.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/stavropol.csv', 'w', encoding='utf-8', newline='') as f:
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
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
    with open('csv/krasnodar.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)



async def parser_cheboksari(dct_up):
    try:
        res_1 = await avto_trend(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://avto-trend21.ru/auto/')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await avto_shop_21(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://auto-shop-21.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await avto_alyans(dct_up)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://alyans-auto.ru/auto/auto.html error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
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
    sheet.cell(row=1, column=6).value = 'avto-trend21.ru'
    sheet.cell(row=1, column=7).value = 'avto-trend21.ru_price'
    sheet.cell(row=1, column=8).value = 'auto-shop-21.ru'
    sheet.cell(row=1, column=9).value = 'auto-shop-21.ru_price'
    sheet.cell(row=1, column=10).value = 'alyans-auto.ru'
    sheet.cell(row=1, column=11).value = 'alyans-auto.ru_price'


    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/cheboksari.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/cheboksari.csv', 'w', encoding='utf-8', newline='') as f:
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
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
    with open('csv/surgut.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_tumen(dct_up, browser):
    try:
        res_1 = await autocentr72(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://autocentr-72.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await bazis_motor(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://bazis-motors.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await tumen_car(dct_up)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://tumen-car.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await china_tumen(dct_up, browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://china-avto-tumen.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await autotumen(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://autotumen.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
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
    sheet.cell(row=1, column=6).value = 'autocentr-72.ru'
    sheet.cell(row=1, column=7).value = 'autocentr-72.ru_price'
    sheet.cell(row=1, column=8).value = 'bazis-motors.ru'
    sheet.cell(row=1, column=9).value = 'bazis-motors.ru_price'
    sheet.cell(row=1, column=10).value = 'tumen-car.ru'
    sheet.cell(row=1, column=11).value = 'tumen-car.ru_price'
    sheet.cell(row=1, column=12).value = 'china-avto-tumen.ru'
    sheet.cell(row=1, column=13).value = 'china-avto-tumen.ru_price'
    sheet.cell(row=1, column=14).value = 'autotumen.ru'
    sheet.cell(row=1, column=15).value = 'autotumen.ru_price'

    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/tumen.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/tumen.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_chelyabinsk(dct_up, browser):
    try:
        res_1 = await ac_aquamarine(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://ac-aquamarine.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await smolino_motors(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://smolino-motors74.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await che_motors(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://che-motors-2024.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await saturn2(dct_up, browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://saturn2.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await avto_mg(dct_up, browser)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://avto-mg.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_6 = await avto_zlt(dct_up, browser)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://avto-zlt.ru/ error')
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
    sheet.cell(row=1, column=6).value = 'ac-aquamarine.ru'
    sheet.cell(row=1, column=7).value = 'ac-aquamarine.ru_price'
    sheet.cell(row=1, column=8).value = 'smolino-motors74.ru'
    sheet.cell(row=1, column=9).value = 'smolino-motors74.ru_price'
    sheet.cell(row=1, column=10).value = 'che-motors-2024.ru'
    sheet.cell(row=1, column=11).value = 'che-motors-2024.ru_price'
    sheet.cell(row=1, column=12).value = 'saturn2.ru'
    sheet.cell(row=1, column=13).value = 'saturn2.ru_price'
    sheet.cell(row=1, column=14).value = 'avto-mg.ru'
    sheet.cell(row=1, column=15).value = 'avto-mg.ru_price'
    sheet.cell(row=1, column=16).value = 'avto-zlt.ru'
    sheet.cell(row=1, column=17).value = 'avto-zlt.ru_price'

    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
    wb.save('xlsx/chelyabinsk.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/chelyabinsk.csv', 'w', encoding='utf-8', newline='') as f:
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
    try:
        await bot.send_message(ADMIN_ID, 'begin https://autodealer-moscow.ru')
        res_9 = await autodealer_moscow(dct_up)
    except Exception as e:
        res_9 = []
        await bot.send_message(CHANEL_ID, 'https://autodealer-moscow.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://az-cars.ru')
        res_10 = await az_cars(dct_up)
    except Exception as e:
        res_10 = []
        await bot.send_message(CHANEL_ID, 'https://az-cars.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8 + res_9 + res_10
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
    res_6_name = [x[0] for x in res_6]
    res_7_name = [x[0] for x in res_7]
    res_8_name = [x[0] for x in res_8]
    res_9_name = [x[0] for x in res_9]
    res_10_name = [x[0] for x in res_10]
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
    sheet.cell(row=1, column=22).value = 'autodealer-moscow.ru'
    sheet.cell(row=1, column=23).value = 'autodealer-moscow.ru_price'
    sheet.cell(row=1, column=24).value = 'az-cars.ru'
    sheet.cell(row=1, column=25).value = 'az-cars.ru_price'
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
        if res_name[i-2] in res_9_name:
            index = res_9_name.index(res_name[i - 2])
            sheet.cell(row=i, column=22).value = res_9[index][1]
            sheet.cell(row=i, column=23).value = res_9[index][2]
            dct[str(res_9[index][1])] = res_9[index][2]
            lst.append(int(res_9[index][1]))
        if res_name[i-2] in res_10_name:
            index = res_10_name.index(res_name[i - 2])
            sheet.cell(row=i, column=24).value = res_10[index][1]
            sheet.cell(row=i, column=25).value = res_10[index][2]
            dct[str(res_10[index][1])] = res_10[index][2]
            lst.append(int(res_10[index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/moscow.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/moscow.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_ufa(dct_up, browser):
    try:
        await bot.send_message(ADMIN_ID, 'begin https://avtolininiya-rb.ru/auto/')
        res_1 = await avto_rb(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://avtolininiya-rb.ru/auto/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://ufa.masmotors.ru/')
        res_2 = await ufa_masmotors(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://ufa.masmotors.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://avrora-motors.ru/catalog')
        res_3 = await avrora(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://avrora-motors.ru/catalog')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://ufa.autospot.ru/')
        res_4 = await ufa_autospot(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://ufa.autospot.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://alfa-tank.ru/')
        res_5 = await alpha_tank(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://alfa-tank.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://autofort-ufa.ru/')
        res_6 = await ufa_autofort(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://autofort-ufa.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://motors-ag.ru/')
        res_7 = await motors_ag(dct_up, browser)
    except Exception as e:
        res_7 = []
        await bot.send_message(CHANEL_ID, 'https://motors-ag.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        await bot.send_message(ADMIN_ID, 'begin https://alga-auto.ru/auto/')
        res_8 = await alga_auto(dct_up)
    except Exception as e:
        res_8 = []
        await bot.send_message(CHANEL_ID, 'https://alga-auto.ru/auto/ error')
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
    sheet.cell(row=1, column=6).value = 'avtolininiya-rb.ru'
    sheet.cell(row=1, column=7).value = 'avtolininiya-rb.ru_price'
    sheet.cell(row=1, column=8).value = 'ufa.masmotors.ru'
    sheet.cell(row=1, column=9).value = 'ufa.masmotors.ru_price'
    sheet.cell(row=1, column=10).value = 'avrora-motors.ru'
    sheet.cell(row=1, column=11).value = 'avrora-motors.ru_price'
    sheet.cell(row=1, column=12).value = 'ufa.autospot.ru'
    sheet.cell(row=1, column=13).value = 'ufa.autospot.ru_price'
    sheet.cell(row=1, column=14).value = 'alfa-tank.ru'
    sheet.cell(row=1, column=15).value = 'alfa-tank.ru_price'
    sheet.cell(row=1, column=16).value = 'autofort-ufa.ru'
    sheet.cell(row=1, column=17).value = 'autofort-ufa.ru_price'
    sheet.cell(row=1, column=18).value = 'motors-ag.ru'
    sheet.cell(row=1, column=19).value = 'motors-ag.ru_price'
    sheet.cell(row=1, column=20).value = 'alga-auto.ru'
    sheet.cell(row=1, column=21).value = 'alga-auto.ru_price'
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
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
    wb.save('xlsx/ufa.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/ufa.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)