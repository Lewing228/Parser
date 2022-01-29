from pickle import TRUE
import requests
from bs4 import BeautifulSoup
import csv
import os
import re


URL = "https://www.sulpak.kz/f/smartfoniy"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'accept' : '*/*'
}
FILE = input('Введите название файла: ') + '.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.select('div.pages-list a')
    if pagination:
        return int(pagination[-1].get_text().replace('\n', ''))
    else:
        return 1
    

    


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("li", class_="tile-container")
    
    phones = []
    for item in items:
        old_price = item.find('div', class_='old-price')
        price = item.find('span', class_='hidden', text='Цена:')
        if old_price:
            old_price = old_price.get_text().replace('₸', '')
        else:
            old_price = 'Скидки нет'
        if price:
            price = price.find_next('span').get_text().replace('₸', '')
        else:
            price = 'Нет в наличии'
        phones.append({
            'title': item.find('h3', class_='title').get_text(strip=TRUE).replace('\n', ''),
            'price': price,
            'old price' : old_price,
        })    
    return phones



def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Модель', 'Цена', 'Цена без скидки'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['old price']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        phones = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            phones.extend(get_content(html.text))
        save_file(phones, FILE)
        print(f'Получено {len(phones)} товаров')
        os.startfile(FILE)
    else: 
        print('Error')

parse()

