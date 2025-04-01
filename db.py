import re
import sqlite3

import pandas as pd
import requests
from lxml import html


def init_db():
    """Инициализация БД."""

    conn = sqlite3.connect('sites.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            xpath TEXT NOT NULL
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS prices (
            site_id INTEGER,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(site_id) REFERENCES sites(id)
        )
        '''
    )
    conn.commit()
    conn.close()


def site_exists(conn, url):
    """Проверка существования сайта в БД."""

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sites WHERE url = ?", (url,))
    return cursor.fetchone()[0] > 0


def save_to_db(df):
    """Сохранение данных из Excel в БД."""

    conn = sqlite3.connect('sites.db')
    cursor = conn.cursor()

    for _, row in df.iterrows():
        if not site_exists(conn, row["url"]):
            cursor.execute(
                'INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)',
                (row['title'], row['url'], row['xpath']),
            )

    conn.commit()
    conn.close()


def clean_price(price_str):
    """Очистка цены от лишних символов."""

    if isinstance(price_str, str):
        return float(re.sub(r'[^\d.]', '', price_str).replace(',', '.'))
    return float(price_str)


def parse_prices():
    """Парсинг цен."""

    conn = sqlite3.connect('sites.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, url, xpath FROM sites')
    sites = cursor.fetchall()
    averages = []

    for site_id, title, url, xpath in sites:
        try:
            response = requests.get(url, timeout=10)
            tree = html.fromstring(response.content)
            price_element = tree.xpath(xpath)

            if not price_element:
                raise ValueError(f'Не найден элемент по XPath: {xpath}')

            price = clean_price(price_element[0].text)

            cursor.execute(
                'INSERT INTO prices (site_id, price) VALUES (?, ?)',
                (site_id, price),
            )

            cursor.execute(
                'SELECT AVG(price) FROM prices WHERE site_id = ?', (site_id,)
            )
            avg_price = cursor.fetchone()[0]

            averages.append(f'{title}: {avg_price:.2f} руб.')

        except Exception as e:
            print(f'Ошибка парсинга {url}: {str(e)}')

    conn.commit()
    conn.close()
    return averages
