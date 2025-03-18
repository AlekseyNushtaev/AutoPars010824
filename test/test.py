import csv
import json
import time
import requests
import bs4
import fake_headers
from selenium.webdriver.common.by import By

from bot import bot
from config import ADMIN_ID, CHANEL_ID
from pprint import pprint

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

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
    dct_id = {}
    for item in data:
        name = item['brand'].lower() + ', ' + item['model'].lower().replace(" ", "")
        print(name)
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
    for region in ['krsk']:
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
            with open(f'../csv/{region}.csv', 'r', encoding='utf-8') as csvfile:
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
                print(baza_vesta)
                if i == 17:
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_xray) // 100) * 100
                if i in [19, 20]:
                    res_lst[i][1] = (int(dct_rrc[i + 1] * baza_largus) // 100) * 100
            pprint(res_lst)
            # for item in res_lst:
            #     res[str(item[0])] = {'min_price': item[1]}
            # json_object = json.dumps(res, indent=4)
            # with open(f'json/{region}.json', 'w') as f:
            #     f.write(json_object)

#
# def newavto_kazan(dct_up):
#     headers = fake_headers.Headers(browser='firefox', os='win')
#     link = 'https://newavto-kazan.ru/auto/'
#     response = requests.get(link, headers.generate())
#     html = response.text
#     soup = bs4.BeautifulSoup(html, 'lxml')
#     cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
#     res = []
#     for card in cards:
#         data = card.get("data-model").replace('null', 'None').replace('\\', '')
#         dct = eval(data)
#         link = 'https://newavto-kazan.ru' + card.find("a").get("href")
#         name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
#         try:
#             name = dct_up[name]
#         except KeyError:
#             # await bot.send_message(CHANEL_ID, f'{name} {link}')
#             print([name, dct["cost"], link])
#         res.append([name, dct["cost"], link])
#         print([name, dct["cost"], link])
#     return res




#
# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
#
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)
# browser.maximize_window()
dct = {}
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        dct[item.split('|')[0].strip()] = item.split('|')[1].strip()
json_maker(dct)
