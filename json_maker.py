import requests
import fake_headers
import json
import csv
from bot import bot
from config import ADMIN_ID, CHANEL_ID

dct_rrc = {
    1: 749900,
    2: 1077000,
    3: 778500,
    4: 719300,
    5: 1175000,
    6: 950900,

    7: 1121900,
    8: 1239900,
    9: 1269900,
    10: 1759000,
    11: 1213900,
    12: 1655000,
    13: 1328900,
    14: 1879000,
    15: 1316900,
    16: 1597900,

    17: 1106900,
    18: 1249900,

    19: 1660000,
    20: 2020000,
    21: 1670000,

    22: 1314000
}
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
    for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd', 'samara', 'kazan', 'spb', 'omsk',
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
            res_lst = []
            res = {}
            with open(f'csv/{region}.csv', 'r', encoding='utf-8') as csvfile:
                lst_file = csv.reader(csvfile)
                for row in lst_file:
                    name = row[0] + ', ' + row[1]
                    if name in dct_id.keys():
                        res_lst.append([dct_id[name], int(row[2])])
            res_lst.sort()
            baza_granta = res_lst[3][1] / dct_rrc[4]
            baza_vesta = res_lst[6][1] / dct_rrc[7]
            baza_xray = res_lst[16][1] / dct_rrc[17]
            baza_largus = res_lst[18][1] / dct_rrc[19]
            for i in range(21):
                if i in [0, 1, 2, 4, 5]:
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_granta) // 100) * 100
                if i in range(7, 16):
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_vesta) // 100) * 100
                if i == 17:
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_xray) // 100) * 100
                if i in [19, 20]:
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_largus) // 100) * 100
            for item in res_lst:
                res[str(item[0])] = {'min_price': item[1]}
            json_object = json.dumps(res, indent=4)
            with open(f'json/{region}.json', 'w') as f:
                f.write(json_object)
