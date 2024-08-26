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
        try:
            dct_id[dct[name]] = item['id']
        except Exception:
            print(name)
            await bot.send_message(CHANEL_ID, f"id {item['id']} - error\nhttp://37.143.15.242/api/v1/models")
    for region in ['krasnodar', 'moscow', 'stavropol', 'surgut', 'volgograd',
                   'chelyabinsk', 'cheboksari', 'ufa', 'tumen', 'ekaterinburg', 'saratov']:
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





