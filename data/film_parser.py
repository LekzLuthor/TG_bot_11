import os
import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import glob


# передается код нужной информации 1 - описание фильма, 2 - ссылки на изображения
def parser(item_code):
    url = 'https://trkslon.ru/kino/schedule-cinema/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data_value = soup.find('div', class_='row')
    headlines = data_value.find_all('span', class_='card__name card__name--cinema')
    description = data_value.find_all('div', class_='card__summary')
    times = data_value.find_all('div', class_='card__time')
    img_links = data_value.find_all('img', class_='img-responsive center-block')

    films_names = [i.text for i in headlines]
    films_description = [item.text for item in description]
    films_time = [i.text for i in times]
    posters_links = ['http://trkslon.ru' + i.get('src') for i in img_links]

    if item_code == 1:
        return films_names, films_description, films_time
    elif item_code == 2:
        return posters_links


def img_installer():
    links = parser(2)
    for i in range(len(links)):
        p = requests.get(links[i])
        out = open(f"/pythonProject1/data/posters/{i}.jpg", 'wb')
        out.write(p.content)
        out.close()


def clear_logs():
    files = glob.glob('/pythonProject1/data/posters/*.jpg')
    for f in files:
        os.remove(f)


# img_installer()
# clear_logs()
