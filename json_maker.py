from pprint import pprint

import openpyxl
import requests
import fake_headers
import json
import csv
from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def json_maker(dct):
    headers = fake_headers.Headers(browser='firefox', os='win')
    try:
        response = requests.get('http://37.143.15.242/api/v1/models', headers.generate())
        data = json.loads(response.text)
    except Exception:
        data = []
        await bot.send_message(ADMIN_ID, 'http://37.143.15.242/api/v1/models error')
    dct_id = {}
    for item in data:
        name = item['brand'].lower() + ', ' + item['model'].lower().replace(" ", "")
        if name == 'haval, jolion':
            name = 'haval, jolion1'
        elif name == 'haval, jolion1':
            name = 'haval, jolion'

        if name == 'geely, atlas':
            name = 'geely, atlas1'
        elif name == 'geely, atlas1':
            name = 'geely, atlas'

        if name == 'geely, coolray':
            name = 'geely, coolray1'
        elif name == 'geely, coolray1':
            name = 'geely, coolray'

        if name == 'lada, vestacross':
            name = 'lada, vestacross1'
        elif name == 'lada, vestacross1':
            name = 'lada, vestacross'

        if name == 'lada, vesta':
            name = 'lada, vesta1'
        elif name == 'lada, vesta1':
            name = 'lada, vesta'

        if name == 'lada, vestasw1':
            name = 'lada, vestasw1'
        elif name == 'lada, vestasw1':
            name = 'lada, vestasw'

        if name == 'lada, vestaswcross1':
            name = 'lada, vestaswcross1'
        elif name == 'lada, vestaswcross1':
            name = 'lada, vestaswcross'

        try:
            dct_id[dct[name]] = item['id']
        except Exception:
            print(name)
            await bot.send_message(CHANEL_ID, f"id {item['id']} - error\nhttp://37.143.15.242/api/v1/models")
    for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd', 'samara', 'kazan', 'spb', 'omsk', 'himki',
                   'chelyabinsk', 'cheboksari', 'ufa', 'tumen', 'ekaterinburg', 'saratov', 'kemerovo', 'nsk', 'krsk']:
        if region != 'krsk':
            res_lst = []
            res = {}
            with open(f'csv/{region}.csv', 'r', encoding='utf-8') as csvfile:
                lst_file = csv.reader(csvfile)
                for row in lst_file:
                    name = row[0] + ', ' + row[1]
                    if name in dct_id.keys():
                        res_lst.append([dct_id[name], int(row[2])])
            res_lst.sort()
            for item in res_lst:
                res[str(item[0])] = {'min_price': item[1]}
            json_object = json.dumps(res, indent=4)
            with open(f'json/{region}.json', 'w') as f:
                f.write(json_object)
        else:
            dct_region = {}
            res_lst = []
            res = {}
            with open(f'csv/{region}.csv', 'r', encoding='utf-8') as csvfile:
                lst_file = list(csv.reader(csvfile))[1:]
                for row in lst_file:
                    name = row[0] + ', ' + row[1]
                    dct_region[name] = int(row[2])
            res_all = []
            wb = openpyxl.load_workbook('id.xlsx')
            sh = wb['Sheet']
            for i in range(1, 1000):
                model_id = sh.cell(i, 4).value
                if model_id:
                    brand = sh.cell(i, 2).value
                    model = sh.cell(i, 3).value
                    name = brand + ', ' + model
                    price_rrc = sh.cell(i, 5).value
                    price_min = dct_region.get(name, 0)
                    res_all.append([model_id, name, price_rrc, price_min])
            res_all.sort(key=lambda x: x[0])
            pprint(res_all)
            for cat in ['Lada, Granta', 'Lada, Vesta', 'Lada, Xray', 'Lada, Largus', 'Chevrolet', 'Datsun', 'Haval',
                        'Hyundai',
                        'KIA', 'Nissan', 'Renault', 'Skoda', 'Volkswagen', 'Changan', 'DFM', 'FAW', 'Geely', 'JAC',
                        'Lifan',
                        'Ravon', 'Zotye', 'Chery', 'OMODA', 'EXEED', 'BAIC', 'Jetta,', 'KAIYI', 'Livan', 'Moskvich',
                        'TANK',
                        'JAECOO', 'Jetour']:
                lst_cat = []
                for model in res_all:
                    if cat in model[1]:
                        lst_cat.append(model)
                lst_cat.sort(key=lambda x: x[2])
                if lst_cat[0][3] == 0:
                    baza = 0.6
                else:
                    baza = lst_cat[0][3] / lst_cat[0][2]
                for car in lst_cat:
                    price_min_fix = (int(baza * car[2]) // 100) * 100
                    res_lst.append([int(car[0]), price_min_fix])
            res_lst.sort(key=lambda x: x[0])
            for item in res_lst:
                res[str(item[0])] = {'min_price': item[1]}
            json_object = json.dumps(res, indent=4)
            with open(f'json/{region}.json', 'w') as f:
                f.write(json_object)
