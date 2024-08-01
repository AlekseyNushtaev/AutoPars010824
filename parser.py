import csv

import openpyxl
from bot import bot
from config import ADMIN_ID
from regions.stavropol import autoshop26
from regions.surgut import autosurgut186, profsouz, aspect, sibir

async def parser_stavropol(dct_up):
    try:
        res = await autoshop26(dct_up)
    except Exception:
        res = []
        await bot.send_message(ADMIN_ID, 'https://autoshop26.ru/auto/')
    res.sort(key=lambda x: x[0])
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet.cell(row=1, column=1).value = 'brand'
    sheet.cell(row=1, column=2).value = 'model'
    sheet.cell(row=1, column=3).value = 'min_price'
    sheet.cell(row=1, column=4).value = 'min_price_url'
    sheet.cell(row=1, column=5).value = 'autoshop26.ru'
    sheet.cell(row=1, column=6).value = 'autoshop26.ru_price'
    for i in range(2, len(res) + 2):
        sheet.cell(row=i, column=1).value = res[i-2][0].split(', ')[0]
        sheet.cell(row=i, column=2).value = res[i-2][0].split(', ')[1]
        sheet.cell(row=i, column=3).value = res[i-2][1]
        sheet.cell(row=i, column=4).value = res[i-2][2]
        sheet.cell(row=i, column=5).value = res[i-2][1]
        sheet.cell(row=i, column=6).value = res[i-2][2]
    wb.save('stavropol.xlsx')
    data = []
    for i in range(1, len(res) + 1):
        string = []
        for y in range(1, 4):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('stavropol.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


async def parser_surgut(dct_up, browser):
    try:
        res_1 = await autosurgut186(dct_up)
    except Exception:
        res_1 = []
        await bot.send_message(ADMIN_ID, 'https://autosurgut186.ru/auto/')
    try:
        res_2 = await profsouz(dct_up, browser)
    except Exception:
        res_2 = []
        await bot.send_message(ADMIN_ID, 'https://auto-centre-profsouz.ru/auto')
    try:
        res_3 = await aspect(dct_up, browser)
    except Exception:
        res_3 = []
        await bot.send_message(ADMIN_ID, 'https://aspect-motors.ru/auto')
    try:
        res_4 = await sibir(dct_up)
    except Exception:
        res_4 = []
        await bot.send_message(ADMIN_ID, 'https://sibir-morots.ru/auto/')
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
    sheet.cell(row=1, column=1).value = 'brand'
    sheet.cell(row=1, column=2).value = 'model'
    sheet.cell(row=1, column=3).value = 'min_price'
    sheet.cell(row=1, column=4).value = 'min_price_url'
    sheet.cell(row=1, column=5).value = 'autosurgut186.ru'
    sheet.cell(row=1, column=6).value = 'autosurgut186.ru_price'
    sheet.cell(row=1, column=7).value = 'auto-centre-profsouz.ru'
    sheet.cell(row=1, column=8).value = 'auto-centre-profsouz.ru_price'
    sheet.cell(row=1, column=9).value = 'aspect-motors.ru'
    sheet.cell(row=1, column=10).value = 'aspect-motors.ru_price'
    sheet.cell(row=1, column=11).value = 'sibir-morots.ru'
    sheet.cell(row=1, column=12).value = 'sibir-morots.ru_price'

    for i in range(2, len(res_name) + 2):
        sheet.cell(row=i, column=1).value = res_name[i-2].split(', ')[0]
        sheet.cell(row=i, column=2).value = res_name[i-2].split(', ')[1]
        dct = {}
        lst = []
        if res_name[i-2] in res_1_name:
            index = res_1_name.index(res_name[i - 2])
            sheet.cell(row=i, column=5).value = res_1[index][1]
            sheet.cell(row=i, column=6).value = res_1[index][2]
            dct[str(res_1[index][1])] = res_1[index][2]
            lst.append(int(res_1[index][1]))
        if res_name[i-2] in res_2_name:
            index = res_2_name.index(res_name[i - 2])
            sheet.cell(row=i, column=7).value = res_2[index][1]
            sheet.cell(row=i, column=8).value = res_2[index][2]
            dct[str(res_2[index][1])] = res_2[index][2]
            lst.append(int(res_2[index][1]))
        if res_name[i-2] in res_3_name:
            index = res_3_name.index(res_name[i - 2])
            sheet.cell(row=i, column=9).value = res_3[index][1]
            sheet.cell(row=i, column=10).value = res_3[index][2]
            dct[str(res_3[index][1])] = res_3[index][2]
            lst.append(int(res_3[index][1]))
        if res_name[i-2] in res_4_name:
            index = res_4_name.index(res_name[i - 2])
            sheet.cell(row=i, column=11).value = res_4[index][1]
            sheet.cell(row=i, column=12).value = res_4[index][2]
            dct[str(res_4[index][1])] = res_4[index][2]
            lst.append(int(res_4[index][1]))
        sheet.cell(row=i, column=3).value = min(lst)
        sheet.cell(row=i, column=4).value = dct[str(min(lst))]
    wb.save('surgut.xlsx')
    data = []
    for i in range(1, len(res_name) + 1):
        string = []
        for y in range(1, 4):
            string.append(sheet.cell(row=i, column=y).value)
        data.append(string)
    with open('surgut.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

