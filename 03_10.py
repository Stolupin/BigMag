import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
from tkinter import *

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'}


def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_='base-pagination__item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div',
                          class_='catalog-products__item product-layout product-list product-layout product-grid')
    phones = []
    for item in items:
        phones.append({'title': item.find('a', class_='product-preview__title').get_text(),
                       'link': item.find('a', class_='product-preview__title').get('href'),
                       'price': item.find('span', class_='product-preview-price__value').get_text()
                       })

    return phones


def but_parsit():
    parse()


def table_name():
    tablica = nazvanie_tablicu.get()
    nazvanie_tablicu.delete(0, tk.END)

    return tablica


def parse():
    URL = pole_dlya_vvoda.get()
    table = table_name()
    try:
        html = get_html(URL)

        if html.status_code == 200:
            phones = []
            pages_count = get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                a = entry.get()
                entry.delete(0, tk.END)
                html = get_html(URL + f'?page={page}')
                phones.extend(get_content(html.text))
                procces.insert(0.0, f'Парсинг страницы {page} из {pages_count} страниц...\n')
                print(a)
            procces.insert(0.0, f'Готово\n ')
    except requests.exceptions.MissingSchema:
        messagebox.showinfo('Ошибка', "Вы не ввели или ввели неверный URL")

        # else:
        #     print('Error')

    def phone():
        try:
            with sq.connect('bigmag.db') as con:

                cur = con.cursor()
                query_c = f"CREATE TABLE IF NOT EXISTS {table}(name TEXT, links TEXT, price TEXT)"
                con.execute(query_c)
                print('Готово')
        except sq.OperationalError:
            messagebox.showinfo('Ошибка', "Вы не ввели название таблицы")
            procces.insert(0.0, f'Данные не спарсились.\n')

        for phone in phones:
            try:
                query_w = f"INSERT INTO {table}(name, links, price) VALUES('{phone['title']}'," \
                          f"'{phone['link']}','{phone['price']}')"
                con.execute(query_w)
                con.commit()
            except sq.Error as error:
                print("Ошибка при добавлении:", error)

    phone()


work = tk.Tk()
work.title('BigMag')
work.geometry("280x280")
work.config(bg='#5B5E61')
work.minsize(280, 280)
work.maxsize(280, 280)
vvedite_url = tk. \
    Label(work, text='Введите URL:', font=('Impact', 9, 'bold'), fg='#36353A', bg='#DEDCE9'). \
    place(x=5, y=5)
entry = tk.Entry(work, justify=tk.LEFT, font=('Impact', 13))
vvedite_name_tablicu = tk.Label(work, text='Таблица:', font=('Impact', 9, 'bold'), fg='#36353A', bg='#DEDCE9'). \
    place(x=5, y=65)
pole_dlya_vvoda = tk.Entry(work, justify=tk.LEFT)
pole_dlya_vvoda.place(x=105, y=5)
nazvanie_tablicu = tk.Entry(work, justify=tk.LEFT)
nazvanie_tablicu.place(x=105, y=65)
nazvanie_tablicu.insert(0, 'F')
procces_label = tk.Label(work, text="Процесс:", font=('Impact', 10, 'bold'), fg='#36353A', bg='#DEDCE9').place(x=5,
                                                                                                               y=115)
procces = Text(width=25, height=25, wrap=WORD, bg='#D2FDCF')
procces.place(x=5, y=140, width=270, height=130)
work.columnconfigure(0, minsize=20)
work.columnconfigure(1, minsize=20)
work.columnconfigure(2, minsize=50)
work.columnconfigure(3, minsize=50)

work.rowconfigure(0, minsize=60)
work.rowconfigure(1, minsize=20)
work.rowconfigure(2, minsize=60)
work.rowconfigure(3, minsize=60)


def clear1():
    pole_dlya_vvoda.delete(0, tk.END)


def clear2():
    nazvanie_tablicu.delete(0, tk.END)


tk.Button(work, text='Очистить', bg='#F95C4B', command=clear1).place(x=105, y=30, width=70, height=30)
tk.Button(work, text='Очистить', bg='#F95C4B', command=clear2).place(x=105, y=90, width=70, height=30)
tk.Button(work, text='Парсинг', bg='#34D129', command=parse).place(x=180, y=90, width=70, height=30)

work.mainloop()

but_parsit()
