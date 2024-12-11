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
from regions.saratov import *
from regions.samara import *
from pprint import pprint


async def parser_ekaterinburg(dct_up, browser):
    try:
        res_1 = await new_auto_96(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://new-auto96.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await auto_196(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://auto-196.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await autosalon_kit(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://autosalon-kit.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await kit_autoshop(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://kit-autoshop.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await primeauto_ekb(dct_up, browser)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://primeauto-ekb.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_6 = await atc_gagarin(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://atc-gagarin.ru error')
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
    sheet.cell(row=1, column=6).value = 'new-auto96.ru_price'
    sheet.cell(row=1, column=7).value = 'new-auto96.ru'
    sheet.cell(row=1, column=8).value = 'auto-196.ru_price'
    sheet.cell(row=1, column=9).value = 'auto-196.ru'
    sheet.cell(row=1, column=10).value = 'autosalon-kit.ru_price'
    sheet.cell(row=1, column=11).value = 'autosalon-kit.ru'
    sheet.cell(row=1, column=12).value = 'kit-autoshop.ru_price'
    sheet.cell(row=1, column=13).value = 'kit-autoshop.ru'
    sheet.cell(row=1, column=14).value = 'primeauto-ekb.ru_price'
    sheet.cell(row=1, column=15).value = 'primeauto-ekb.ru'
    sheet.cell(row=1, column=16).value = 'atc-gagarin.ru_price'
    sheet.cell(row=1, column=17).value = 'atc-gagarin.ru'
    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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


async def parser_saratov(dct_up):
    try:
        res_1 = await saratov_avtohous(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://saratov-avtohous.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await cartrade_saratov(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://cartrade-saratov.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await autodealer_saratov(dct_up)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://autodealer-saratov.ru error')
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
    sheet.cell(row=1, column=6).value = 'saratov-avtohous.ru_price'
    sheet.cell(row=1, column=7).value = 'saratov-avtohous.ru'
    sheet.cell(row=1, column=8).value = 'cartrade-saratov.ru_price'
    sheet.cell(row=1, column=9).value = 'cartrade-saratov.ru'
    sheet.cell(row=1, column=10).value = 'autodealer-saratov.ru_price'
    sheet.cell(row=1, column=11).value = 'autodealer-saratov.ru'
    lst_res = [res_1, res_2, res_3]
    lst_res_name = [res_1_name, res_2_name, res_3_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/saratov.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/saratov.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_samara(dct_up, browser):
    try:
        res_1 = await park_auto_sm(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://park-auto-sm.ru error')
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
    sheet.cell(row=1, column=6).value = 'park-auto-sm.ru_price'
    sheet.cell(row=1, column=7).value = 'park-auto-sm.ru'
    lst_res = [res_1]
    lst_res_name = [res_1_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
        sheet.cell(row=i, column=4).value = min(lst)
        sheet.cell(row=i, column=5).value = dct[str(min(lst))]
    wb.save('xlsx/samara.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(2, 5):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('csv/samara.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_volgograd(dct_up, browser):
    try:
        res_1 = await vlg_auto34(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://vlg-auto34.ru error')
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
    sheet.cell(row=1, column=6).value = 'https://vlg-auto34.ru_price'
    sheet.cell(row=1, column=7).value = 'https://vlg-auto34.ru'
    lst_res = [res_1]
    lst_res_name = [res_1_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        res_1 = await autocenter_stav(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://autocenter-stav.ru/auto/ error')
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
    sheet.cell(row=1, column=6).value = 'autocenter-stav.ru_price'
    sheet.cell(row=1, column=7).value = 'autocenter-stav.ru'
    lst_res = [res_1]
    lst_res_name = [res_1_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        res_1 = await car_kranodar(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://car-krasnodar.ru/cars/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await avangard_yug(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://avangard-yug.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await rostov_avto(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://rostov-avto-1.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await krd_93_car(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://krd93-car.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await maximum_auto_credit(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://maximum-auto-credit.ru error')
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
    sheet.cell(row=1, column=6).value = 'car-krasnodar.ru_price'
    sheet.cell(row=1, column=7).value = 'car-krasnodar.ru'
    sheet.cell(row=1, column=8).value = 'avangard-yug.ru_price'
    sheet.cell(row=1, column=9).value = 'avangard-yug.ru'
    sheet.cell(row=1, column=10).value = 'rostov-avto-1.ru_price'
    sheet.cell(row=1, column=11).value = 'rostov-avto-1.ru'
    sheet.cell(row=1, column=12).value = 'krd93-car.ru_price'
    sheet.cell(row=1, column=13).value = 'krd93-car.ru'
    sheet.cell(row=1, column=14).value = 'maximum-auto-credit.ru_price'
    sheet.cell(row=1, column=15).value = 'maximum-auto-credit.ru'

    lst_res = [res_1, res_2, res_3, res_4, res_5]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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



async def parser_cheboksari(dct_up, browser):
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
    try:
        res_4 = await zd_auto(dct_up, browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://zd-auto.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3
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
    sheet.cell(row=1, column=6).value = 'avto-trend21.ru_price'
    sheet.cell(row=1, column=7).value = 'avto-trend21.ru'
    sheet.cell(row=1, column=8).value = 'auto-shop-21.ru_price'
    sheet.cell(row=1, column=9).value = 'auto-shop-21.ru'
    sheet.cell(row=1, column=10).value = 'alyans-auto.ru_price'
    sheet.cell(row=1, column=11).value = 'alyans-auto.ru'
    sheet.cell(row=1, column=12).value = 'https://zd-auto.ru_price'
    sheet.cell(row=1, column=13).value = 'https://zd-auto.ru'

    lst_res = [res_1, res_2, res_3, res_4]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        res_3 = await sibir(dct_up)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://sibir-morots.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await avtosalon_profsouz(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://avtosalon-profsouz.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await autocentrsurgut186(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://autocentersurgut186.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_6 = await autosalon_hmao(dct_up, browser)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://autosalon-hmao.ru error')
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
    sheet.cell(row=1, column=6).value = 'autosurgut186.ru_price'
    sheet.cell(row=1, column=7).value = 'autosurgut186.ru'
    sheet.cell(row=1, column=8).value = 'auto-centre-profsouz.ru_price'
    sheet.cell(row=1, column=9).value = 'auto-centre-profsouz.ru'
    sheet.cell(row=1, column=10).value = 'sibir-morots.ru_price'
    sheet.cell(row=1, column=11).value = 'sibir-morots.ru'
    sheet.cell(row=1, column=12).value = 'avtosalon-profsouz.ru_price'
    sheet.cell(row=1, column=13).value = 'avtosalon-profsouz.ru'
    sheet.cell(row=1, column=14).value = 'autocentersurgut186.ru_price'
    sheet.cell(row=1, column=15).value = 'autocentersurgut186.ru'
    sheet.cell(row=1, column=16).value = 'autosalon-hmao.ru_price'
    sheet.cell(row=1, column=17).value = 'autosalon-hmao.ru'

    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
    try:
        res_6 = await avtosrf(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://avtosrf5-11.ru error')
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
    sheet.cell(row=1, column=6).value = 'autocentr-72.ru_price'
    sheet.cell(row=1, column=7).value = 'autocentr-72.ru'
    sheet.cell(row=1, column=8).value = 'bazis-motors.ru_price'
    sheet.cell(row=1, column=9).value = 'bazis-motors.ru'
    sheet.cell(row=1, column=10).value = 'tumen-car.ru_price'
    sheet.cell(row=1, column=11).value = 'tumen-car.ru'
    sheet.cell(row=1, column=12).value = 'china-avto-tumen.ru_price'
    sheet.cell(row=1, column=13).value = 'china-avto-tumen.ru'
    sheet.cell(row=1, column=14).value = 'autotumen.ru_price'
    sheet.cell(row=1, column=15).value = 'autotumen.ru'
    sheet.cell(row=1, column=16).value = 'avtosrf5-11.ru_price'
    sheet.cell(row=1, column=17).value = 'avtosrf5-11.ru'

    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        res_1 = await avto_graf(dct_up, browser)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://avto-graf-newcars.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_2 = await che_motors(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://che-motors-2024.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_3 = await saturn2(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://saturn2.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_4 = await ac_174auto(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://ac-174auto.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_5 = await kc_klassavto(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://kc-klassavto.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_6 = await carsklad_174(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://carsklad-174.ru/auto error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_7 = await mnogo_auto_174(dct_up)
    except Exception as e:
        res_7 = []
        await bot.send_message(CHANEL_ID, 'https://mnogo-auto174.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
    res_6_name = [x[0] for x in res_6]
    res_7_name = [x[0] for x in res_7]
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
    sheet.cell(row=1, column=6).value = 'avto-graf-newcars.ru_price'
    sheet.cell(row=1, column=7).value = 'avto-graf-newcars.ru'
    sheet.cell(row=1, column=8).value = 'che-motors-2024.ru_price'
    sheet.cell(row=1, column=9).value = 'che-motors-2024.ru'
    sheet.cell(row=1, column=10).value = 'saturn2.ru_price'
    sheet.cell(row=1, column=11).value = 'saturn2.ru'
    sheet.cell(row=1, column=12).value = 'ac-174auto.ru_price'
    sheet.cell(row=1, column=13).value = 'ac-174auto.ru'
    sheet.cell(row=1, column=14).value = 'kc-klassavto.ru_price'
    sheet.cell(row=1, column=15).value = 'kc-klassavto.ru'
    sheet.cell(row=1, column=16).value = 'carsklad-174.ru_price'
    sheet.cell(row=1, column=17).value = 'carsklad-174.ru'
    sheet.cell(row=1, column=18).value = 'mnogo-auto174.ru_price'
    sheet.cell(row=1, column=19).value = 'mnogo-auto174.ru'
    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6, res_7]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name, res_7_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        # await bot.send_message(ADMIN_ID, 'begin https://nord-car.ru/catalog')
        res_1 = await nord_car(dct_up)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://nord-car.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://dc-dbr.ru/catalog')
        res_2 = await dc_dbr(dct_up)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://dc-dbr.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://you-auto-credit.ru/cars-new/?page=50')
        res_3 = await you_auto_credit(dct_up)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://you-auto-credit.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://warshauto.ru/')
        res_4 = await warshauto(dct_up, browser)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://warshauto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://kosmos-cars.ru/')
        res_5 = await kosmos_cars(dct_up)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://kosmos-cars.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://idol-avto.ru/cars-new/?page=100')
        res_6 = await idol_avto(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://idol-avto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://vita-auto.ru/')
        res_7 = await vita_avto(dct_up)
    except Exception as e:
        res_7 = []
        await bot.send_message(CHANEL_ID, 'https://vita-auto.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://alcon-auto.ru')
        res_8 = await alcon_avto(dct_up, browser)
    except Exception as e:
        res_8 = []
        await bot.send_message(CHANEL_ID, 'https://alcon-auto.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://autodrive-777.ru/auto/')
        res_9 = await autodrive_777(dct_up)
    except Exception as e:
        res_9 = []
        await bot.send_message(CHANEL_ID, 'https://autodrive-777.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://az-cars.ru')
        res_10 = await az_cars(dct_up)
    except Exception as e:
        res_10 = []
        await bot.send_message(CHANEL_ID, 'https://az-cars.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'https://avtohous-group.ru/katalog')
        res_11 = await autohous_group(dct_up)
    except Exception as e:
        res_11 = []
        await bot.send_message(CHANEL_ID, 'https://avtohous-group.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://msk-carshop777.ru/auto/')
        res_12 = await msk_carshop777(dct_up)
    except Exception as e:
        res_12 = []
        await bot.send_message(CHANEL_ID, 'https://msk-carshop777.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_13 = await moscowautos777(dct_up)
    except Exception as e:
        res_13 = []
        await bot.send_message(CHANEL_ID, 'https://moscowautos777.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_14 = await fair_cars(dct_up)
    except Exception as e:
        res_14 = []
        await bot.send_message(CHANEL_ID, 'https://fair-cars.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        res_15 = await avanta_avto_credit(dct_up)
    except Exception as e:
        res_15 = []
        await bot.send_message(CHANEL_ID, 'https://avanta-avto-credit.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8 + res_9 + res_10 + res_11 + res_12 + res_13 + res_14 + res_15
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
    res_11_name = [x[0] for x in res_11]
    res_12_name = [x[0] for x in res_12]
    res_13_name = [x[0] for x in res_13]
    res_14_name = [x[0] for x in res_14]
    res_15_name = [x[0] for x in res_15]
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
    sheet.cell(row=1, column=6).value = 'nord-car.ru_price'
    sheet.cell(row=1, column=7).value = 'nord-car.ru'
    sheet.cell(row=1, column=8).value = 'dc-dbr.ru_price'
    sheet.cell(row=1, column=9).value = 'dc-dbr.ru'
    sheet.cell(row=1, column=10).value = 'you-auto-credit.ru_price'
    sheet.cell(row=1, column=11).value = 'you-auto-credit.ru'
    sheet.cell(row=1, column=12).value = 'warshauto.ru_price'
    sheet.cell(row=1, column=13).value = 'warshauto.ru'
    sheet.cell(row=1, column=14).value = 'kosmos-cars.ru_price'
    sheet.cell(row=1, column=15).value = 'kosmos-cars.ru'
    sheet.cell(row=1, column=16).value = 'idol-avto.ru_price'
    sheet.cell(row=1, column=17).value = 'idol-avto.ru'
    sheet.cell(row=1, column=18).value = 'vita-auto.ru_price'
    sheet.cell(row=1, column=19).value = 'vita-auto.ru'
    sheet.cell(row=1, column=20).value = 'alcon-auto.ru_price'
    sheet.cell(row=1, column=21).value = 'alcon-auto.ru'
    sheet.cell(row=1, column=22).value = 'autodrive-777.ru_price'
    sheet.cell(row=1, column=23).value = 'autodrive-777.ru'
    sheet.cell(row=1, column=24).value = 'az-cars.ru_price'
    sheet.cell(row=1, column=25).value = 'az-cars.ru'
    sheet.cell(row=1, column=26).value = 'avtohous-group.ru_price'
    sheet.cell(row=1, column=27).value = 'avtohous-group.ru'
    sheet.cell(row=1, column=28).value = 'msk-carshop777.ru_price'
    sheet.cell(row=1, column=29).value = 'msk-carshop777.ru'
    sheet.cell(row=1, column=30).value = 'moscowautos777.ru_price'
    sheet.cell(row=1, column=31).value = 'moscowautos777.ru'
    sheet.cell(row=1, column=32).value = 'fair-cars.ru_price'
    sheet.cell(row=1, column=33).value = 'fair-cars.ru'
    sheet.cell(row=1, column=34).value = 'avanta-avto-credit.ru_price'
    sheet.cell(row=1, column=35).value = 'avanta-avto-credit.ru'
    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6, res_7, res_8, res_9, res_10, res_11, res_12, res_13, res_14,
               res_15]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name, res_7_name, res_8_name,
                    res_9_name, res_10_name, res_11_name, res_12_name, res_13_name, res_14_name, res_15_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i-2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i-2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i-2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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
        # await bot.send_message(ADMIN_ID, 'begin https://bashautomarket.ru')
        res_1= await bashautomarket(dct_up, browser)
    except Exception as e:
        res_1 = []
        await bot.send_message(CHANEL_ID, 'https://bashautomarket.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://ufa.masmotors.ru/')
        res_2 = await ufa_masmotors(dct_up, browser)
    except Exception as e:
        res_2 = []
        await bot.send_message(CHANEL_ID, 'https://ufa.masmotors.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://avrora-motors.ru/catalog')
        res_3 = await avrora(dct_up, browser)
    except Exception as e:
        res_3 = []
        await bot.send_message(CHANEL_ID, 'https://avrora-motors.ru/catalog error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://ufa.autospot.ru/')
        res_4 = await ufa_autospot(dct_up)
    except Exception as e:
        res_4 = []
        await bot.send_message(CHANEL_ID, 'https://ufa.autospot.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://alfa-tank.ru/')
        res_5 = await alpha_tank(dct_up, browser)
    except Exception as e:
        res_5 = []
        await bot.send_message(CHANEL_ID, 'https://alfa-tank.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://autofort-ufa.ru/')
        res_6 = await ufa_autofort(dct_up)
    except Exception as e:
        res_6 = []
        await bot.send_message(CHANEL_ID, 'https://autofort-ufa.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://motors-ag.ru/')
        res_7 = await motors_ag(dct_up, browser)
    except Exception as e:
        res_7 = []
        await bot.send_message(CHANEL_ID, 'https://motors-ag.ru/ error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
        # await bot.send_message(ADMIN_ID, 'begin https://ufabm.ru')
        res_8 = await ufabm(dct_up)
    except Exception as e:
        res_8 = []
        await bot.send_message(CHANEL_ID, 'https://ufabm.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    try:
    #     await bot.send_message(ADMIN_ID, 'begin https://ufa-automarket.ru')
        res_9 = await ufa_automarket(dct_up, browser)
    except Exception as e:
        res_9 = []
        await bot.send_message(CHANEL_ID, 'https://ufa-automarket.ru error')
        await bot.send_message(ADMIN_ID, str(e))
    res = res_1 + res_2 + res_3 + res_4 + res_5 + res_6 + res_7 + res_8 + res_9
    res_1_name = [x[0] for x in res_1]
    res_2_name = [x[0] for x in res_2]
    res_3_name = [x[0] for x in res_3]
    res_4_name = [x[0] for x in res_4]
    res_5_name = [x[0] for x in res_5]
    res_6_name = [x[0] for x in res_6]
    res_7_name = [x[0] for x in res_7]
    res_8_name = [x[0] for x in res_8]
    res_9_name = [x[0] for x in res_9]
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
    sheet.cell(row=1, column=6).value = 'bashautomarket.ru_price'
    sheet.cell(row=1, column=7).value = 'bashautomarket.ru.ru'
    sheet.cell(row=1, column=8).value = 'ufa.masmotors.ru_price'
    sheet.cell(row=1, column=9).value = 'ufa.masmotors.ru'
    sheet.cell(row=1, column=10).value = 'avrora-motors.ru_price'
    sheet.cell(row=1, column=11).value = 'avrora-motors.ru'
    sheet.cell(row=1, column=12).value = 'ufa.autospot.ru_price'
    sheet.cell(row=1, column=13).value = 'ufa.autospot.ru'
    sheet.cell(row=1, column=14).value = 'alfa-tank.ru_price'
    sheet.cell(row=1, column=15).value = 'alfa-tank.ru'
    sheet.cell(row=1, column=16).value = 'autofort-ufa.ru_price'
    sheet.cell(row=1, column=17).value = 'autofort-ufa.ru'
    sheet.cell(row=1, column=18).value = 'motors-ag.ru_price'
    sheet.cell(row=1, column=19).value = 'motors-ag.ru'
    sheet.cell(row=1, column=20).value = 'ufabm.ru_price'
    sheet.cell(row=1, column=21).value = 'ufabm.ru'
    sheet.cell(row=1, column=22).value = 'ufa-automarket.ru_price'
    sheet.cell(row=1, column=23).value = 'ufa-automarket.ru'
    lst_res = [res_1, res_2, res_3, res_4, res_5, res_6, res_7, res_8, res_9]
    lst_res_name = [res_1_name, res_2_name, res_3_name, res_4_name, res_5_name, res_6_name, res_7_name, res_8_name,
                    res_9_name]
    for i in range(2, len(res_name) + 2):
        try:
            sheet.cell(row=i, column=1).value = dct_id[res_name[i - 2].strip()]
        except Exception:
            sheet.cell(row=i, column=1).value = 'Новая машина, необходимо назначить id'
        sheet.cell(row=i, column=2).value = res_name[i - 2].split(', ')[0]
        sheet.cell(row=i, column=3).value = res_name[i - 2].split(', ')[1]
        dct = {}
        lst = []
        for y in range(len(lst_res_name)):
            if res_name[i - 2] in lst_res_name[y]:
                index = lst_res_name[y].index(res_name[i - 2])
                sheet.cell(row=i, column=6 + y * 2).value = lst_res[y][index][1]
                sheet.cell(row=i, column=7 + y * 2).value = lst_res[y][index][2]
                dct[str(lst_res[y][index][1])] = lst_res[y][index][2]
                lst.append(int(lst_res[y][index][1]))
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