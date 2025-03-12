import fake_headers
import pandas as pd
import requests
import time
import json
import re


from bs4 import BeautifulSoup

from tqdm import tqdm
from transliterate import translit

from bot import bot
from config import ADMIN_ID


def get_soup(url):
    headers = fake_headers.Headers(browser='firefox', os='win')
    return BeautifulSoup(requests.get(url, headers=headers.generate()).text, 'lxml')


brands_dict = {}


def get_brand_id(brand):
    if not brand in brands_dict.keys():
        brands_dict[brand] = len(brands_dict.keys())
    return brands_dict[brand]


async def parse_mainpage(url):
    SITE = url[:-1]

    soup = get_soup(url)
    try:
        brands = soup.find_all(class_='logobar--brand')
        data = pd.DataFrame()

        for brand in tqdm(brands):
            try:
                soup = get_soup(f"{SITE}{brand.find('a')['href']}")
                cards = soup.find_all(class_='catalog--brands-list--brand--model-card')

                for card in cards:
                    row = pd.DataFrame()

                    row.loc[0, 'brand'] = brand.text.strip()
                    row.loc[0, 'url'] = f"{SITE}{card.find('a')['href']}"
                    row.loc[0, 'name'] = card.find(class_='brand-model').text.strip()
                    row.loc[0, 'old_price'] = int(
                        card.find(class_='price-old rub').text.strip().replace(u'\xa0', '').replace('от',
                                                                                                    '')) if card.find(
                        class_='price-old rub') else None
                    row.loc[0, 'new_price'] = int(
                        card.find(class_='price-new mt-2 rub').text.strip().replace(u'\xa0', '').replace('от', ''))
                    row.loc[0, 'img_url'] = f"{SITE}{card.find('img')['src']}"

                    data = pd.concat([data, row])
            except:
                await bot.send_message(ADMIN_ID, f"Для бренда {brand.find('a')['href']} не найдены машины на сайте: {SITE}")

        data = data.reset_index(drop=True)

        return data, SITE
    except:
        await bot.send_message(ADMIN_ID, f'Не найден каталог брендов на сайте: {SITE}')


async def parse_catalog(data, SITE):
    result = []
    colorshex = []
    for i in tqdm(data.index):  # data.index
        try:
            url = data.loc[i, 'url']
            soup = get_soup(url)
            car = {
                'brand': data.loc[i, 'brand'],
                'brand_alias': data.loc[i, 'url'].split('/')[-3],
                'brand_sort_order': get_brand_id(data.loc[i, 'brand']),

                'model_full': data.loc[i, 'name'].replace(data.loc[i, 'brand'], '').strip(),
                'model_alias': data.loc[i, 'url'].split('/')[-2],

                'body': soup.find(class_='color-text-blur font-500').text.strip() if soup.find(
                    class_='color-text-blur font-500') else soup.find(class_='color-text-blur').text.strip(),
                'body_alias': translit(soup.find(class_='color-text-blur font-500').text.strip(),
                                       reversed=True).lower() if soup.find(class_='color-text-blur font-500') else translit(
                    soup.find(class_='color-text-blur').text.strip(), reversed=True).lower(),

                # 'seats': 5,  #
                # 'doors': 5,  #
                'img_url': data.loc[i, 'img_url'],

                'prices': [],
                'colors': [],
                'galleries': []
            }

            photos = soup.find_all(class_='catalog--model--gallery-thumbnail')
            i = 0
            for photo in photos:
                photo_dict = {
                    'url': f"{SITE}{photo['href']}",
                    'type': photo['data-img-type'],
                    'sort_order': i
                }
                i += 1
                car['galleries'].append(photo_dict)

            color_imgs = soup.find(class_='catalog--model--colors-widget--carousel').find_all('img')
            colors = soup.find(class_='catalog--model--colors-widget--swatches').find_all('div')
            for color in colors:
                if '#' in color['style']:
                    for color_img in color_imgs:
                        try:
                            if color_img['class'][0].replace('color-', '') == color['data-color-id']:
                                color_url = f"{SITE}{color_img['data-src']}"
                        except Exception as e:
                            pass
                    color_dict = {
                        'name': None,  #
                        'colorhex': color['style'].replace('background-color: ', '').replace(';', ''),
                        'img_url': color_url
                    }
                    colorshex.append(color['style'].replace('background-color: ', ''))
                    car['colors'].append(color_dict)

            mods_l = soup.find_all(class_='catalog--model--price-widget--modification')
            for mod_l in mods_l:
                mods = mod_l.find_all(class_='catalog--model--price-widget--modification--price-position')
                for mod in mods:
                    mod_dict = {
                        'complectation': mod.find(
                            class_='catalog--model--price-widget--col-complectation flex align-center xs4 md3 pr-2').text.strip(),
                        'complectation_alias': re.sub(r'[^\w\s]', '', mod.find(
                            class_='catalog--model--price-widget--col-complectation flex align-center xs4 md3 pr-2').text.strip()).lower().replace(
                            ' ', '_'),
                        'cost': int(mod.find(class_='catalog--model--price-widget--col-oldcost xs4 display-xsonly-hidden px-2').text.strip()) if len(mod.find(class_='catalog--model--price-widget--col-oldcost xs4 display-xsonly-hidden px-2').text)>3 else None,
                        'cost_discount': int(
                            mod.find(class_='catalog--model--price-widget--col-cost-value rub').text.strip()),
                    }

                    techs = mod.find_all(class_='flex align-center catalog--model--price-widget--section-row')
                    for tech in techs:
                        if tech.contents[1].text.strip() == 'Тип кузова':
                            mod_dict['body'] = tech.contents[3].text.strip() if tech.contents[3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Двери':
                            mod_dict['doors'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Тип топлива':
                            mod_dict['engine_type'] = tech.contents[3].text.strip() if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Объем двигателя, см3':
                            mod_dict['engine_volume'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else 0
                        if tech.contents[1].text.strip() == 'Мощность двигателя, л.с.':
                            mod_dict['engine_power'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Крутящий момент':
                            mod_dict['engine_torque'] = tech.contents[3].text.strip() if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Топливо':
                            mod_dict['fuel'] = tech.contents[3].text.strip() if tech.contents[3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Тип трансмиссии':
                            mod_dict['gearbox'] = tech.contents[3].text.strip() if tech.contents[3].text.strip() else None
                            mod_dict['gearbox_auto'] = 1 if tech.contents[3].text.strip() == 'Автомат' else 0
                        if tech.contents[1].text.strip() == 'Количество передач':
                            mod_dict['gears'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Привод':
                            mod_dict['transmission'] = tech.contents[3].text.strip() if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Габариты, мм':
                            mod_dict['dim_length'] = int(tech.contents[3].text.strip().split('/')[0]) if tech.contents[
                                3].text.strip() else None
                            mod_dict['dim_width'] = int(tech.contents[3].text.strip().split('/')[1]) if tech.contents[
                                3].text.strip() else None
                            mod_dict['dim_height'] = int(tech.contents[3].text.strip().split('/')[2]) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Дорожный просвет, мм':
                            mod_dict['clearence'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Колесная база, мм':
                            mod_dict['dim_base'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Количество мест':
                            mod_dict['seats'] = tech.contents[3].text.strip() if tech.contents[3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Объем багажника, л.':
                            mod_dict['luggage'] = int(tech.contents[3].text.strip().split('/')[0]) if tech.contents[
                                3].text.strip() else None
                            mod_dict['luggage_max'] = int(tech.contents[3].text.strip().split('/')[0]) if tech.contents[
                                3].text.strip() else None
                            mod_dict['luggage_text'] = f"{tech.contents[3].text.strip().split('/')[0]} л" if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Максимальная скорость, км/ч':
                            mod_dict['max_speed'] = int(tech.contents[3].text.strip()) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Разгон 0-100 км/ч, ч':
                            mod_dict['acceleration'] = round(float(tech.contents[3].text.strip()), 1) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Город, л/100 км':
                            mod_dict['consumption_city'] = round(float(tech.contents[3].text.strip()), 1) if tech.contents[
                                3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Трасса, л/100 км':
                            mod_dict['consumption_highway'] = round(float(tech.contents[3].text.strip()), 1) if \
                                tech.contents[3].text.strip() else None
                        if tech.contents[1].text.strip() == 'Смешанный цикл, л/100 км':
                            mod_dict['consumption_mixed'] = round(float(tech.contents[3].text.strip()), 1) if tech.contents[
                                3].text.strip() else None
                    mod_dict['active'] = 1

                    mod_dict['equipments'] = []
                    eqs = mod.find(
                        class_='flex wrap catalog--model--price-widget--modification--price-position--readmore-container').contents[
                        3].find_all(class_='flex align-center catalog--model--price-widget--section-row')
                    i = 0
                    for eq in eqs:
                        eq_dict = {
                            # 'group_name': None,
                            'name': eq.contents[1].text.strip(),
                            'sort_order': i,
                            'price': None if eq.contents[3].text.strip() == 'Есть' or eq.contents[3].text.strip() == '' or
                                             eq.contents[3].text.strip() == 'Опция' else int(
                                eq.contents[3].text.strip().replace(u'\xa0', '').replace('₽', ''))
                        }
                        i += 1
                        mod_dict['equipments'].append(eq_dict)
                    car['prices'].append(mod_dict)

            result.append(car)
            time.sleep(1)
        except Exception as e:
            await bot.send_message(ADMIN_ID, f"Ошибка при парсинге авто {data.loc[i, 'url']}\n{e}")

    save_url = ''
    try:
        for car in result:
            to_del = []
            for i in range(len(car['colors'])):
                if car['colors'][i]['img_url'] == save_url:
                    car['colors'][i - 1]['colorhex2'] = car['colors'][i]['colorhex']
                    to_del.append(car['colors'][i])
                else:
                    car['colors'][i]['colorhex2'] = None
                    save_url = car['colors'][i]['img_url']
            for d in to_del:
                car['colors'].remove(d)
    except Exception as e:
        await bot.send_message(ADMIN_ID, f"Ошибка при форматировании выходного файла для сайта {SITE}\n{e}")

    return result


def save_result_json(result, filename):
    with open(f'carparser/result_{filename}.json', 'w') as file:
        json.dump(result, file, indent=4)


async def parser_models():
        try:
            url = 'https://autosurgut186.ru/'
            data, SITE = await parse_mainpage(url)
            result = await parse_catalog(data, SITE)
            if result:
                save_result_json(result, 'autosurgut186')
                with open('carparser/result_autosurgut186.json', 'r', encoding='utf-8') as f:
                    lst = json.load(f)
                with open('carparser/geelycityray.json', 'r', encoding='utf-8') as f:
                    cityray = json.load(f)
                with open('carparser/geelypreface.json', 'r', encoding='utf-8') as f:
                    preface = json.load(f)
                models = lst + [cityray] + [preface]
                with open('carparser/models.json', 'w', encoding='utf-8') as f:
                    json.dump(models, f, indent=4)
            else:
                await bot.send_message(ADMIN_ID, f"Ошибка! Выходной файл для сайта autosurgut186.ru не был сохранён!")
        except Exception as e:
            await bot.send_message(ADMIN_ID, f"Ошибка! Парсинга autosurgut186.ru")
