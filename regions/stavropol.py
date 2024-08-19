import requests
import bs4
import fake_headers

from bot import bot
from config import ADMIN_ID, CHANEL_ID


async def autoshop26(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autoshop26.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autoshop26.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


async def autocenter_stav(dct_up):
    headers = fake_headers.Headers(browser='firefox', os='win')
    link = 'https://autocenter-stav.ru/auto/'
    response = requests.get(link, headers.generate())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": "catalog--brands-list--brand--model"})
    res = []
    for card in cards:
        data = card.get("data-model").replace('null', 'None').replace('\\', '')
        dct = eval(data)
        link = 'https://autocenter-stav.ru' + card.find("a").get("href")
        name = dct["brand"].lower() + ', ' + dct["model"].lower().replace(" ", "")
        try:
            name = dct_up[name]
        except KeyError:
            await bot.send_message(CHANEL_ID, f'{name} {link}')
        res.append([name, dct["cost"], link])
    return res


# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)
# start = datetime.datetime.now()
# res = autocenter_stav({})
# # print(datetime.datetime.now() - start)
# res_name = []
# with open('../autolist.txt', 'r', encoding='utf-8') as f:
#     lst = f.readlines()
#     for item in lst:
#         title = item.split('|')[0].strip()
#         res_name.append(title)
# for i in res:
#     if i[0] not in res_name:
#         print(i)