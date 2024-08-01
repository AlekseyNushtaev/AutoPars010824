import requests
import bs4
import fake_headers

def autoshop26():
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
        res.append([dct["brand"].lower() + ', ' + dct["model"].lower(), dct["cost"], link])
    return res
