
import requests
from bs4 import BeautifulSoup
import os
import sqlite3

if os.path.exists('mydatabase.db') == True:
    os.remove("mydatabase.db")#Удаляем старый файл если он существует

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# Создание таблицы

cursor.execute("""PRAGMA foreign_keys=on;""")# разрешаем создание внешних ключей
cursor.execute(""" CREATE TABLE Sofa (ID integer PRIMARY KEY, Артикул integer NOT NULL, Доступность text NOT NULL, FOREIGN KEY (Артикул) REFERENCES Vendor(Артикул), UNIQUE (ID) ON CONFLICT IGNORE)""")
cursor.execute(""" CREATE TABLE Vendor (Артикул integer PRIMARY KEY, Название text NOT NULL, цена integer NOT NULL, СоСкидкой integer, UNIQUE (Артикул) ON CONFLICT IGNORE) """)


url = 'https://azbykamebeli.ru/catalog/0000057/'# прямые диваны
n = 1
while url != None:# считывание страниц со списками диванов
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')  # весь код страницы
    items = soup.find_all('div', class_='col-lg-3 col-md-4 col-sm-6 mb-3 fadeInUp') #список диванов
    for n, i in enumerate(items, start=n): #перебор диванов на странице
        item_text = i.find('div', class_='d-flex justify-content-between').text.strip() #код с артиклем и статусом
        article = item_text.splitlines()[0] #артикул
        item_available = item_text.splitlines()[1] #статус
        item_name = i.find('h4', class_='item__title').text.strip() #название дивана
        item_price_text = i.find('div', class_='price').text.strip() #код с ценами на диван
        item_price_discount = item_price_text.splitlines()[0] #цена без скидки
        if (len(item_price_text.splitlines()) > 1):
            item_price_nondiscount = item_price_text.splitlines()[1] #цена со скидкой если она есть
        else:item_price_nondiscount = '0' #если скидки нет - заполняем значением обычной цены
        #-----------------------------------------------------------------------------------------------------------------
        # получение id со страницы дивана
       # internal_link ='https://azbykamebeli.ru' + i.find('a').get('href') #получаем ссылку на карточку дивана
       # response_item = requests.get(internal_link)
       # soup_item = BeautifulSoup(response_item.text, 'lxml')  # весь код страницы
       # Info_item = soup_item.find('div', class_='align-self-start').text.strip()
       # ID_item = Info_item.splitlines()[1]  # статус
        #-----------------------------------------------------------------------------------------------------------------
        ID_item = i.find('a').get('href').split('Id=')[1] # получаем id из ссылки на карточку дивана

        sqlite_insert_with_param1 = """INSERT OR IGNORE INTO Vendor (Артикул, Название , цена , СоСкидкой) VALUES (?,?,?,?);"""
        data_tuple1 = (int(article[article.find(":") + 1:]), item_name, int((item_price_discount.partition('₽')[0]).replace(' ', '')), int(item_price_nondiscount.partition('₽')[0].replace(' ', '')))
        sqlite_insert_with_param2 = """INSERT OR IGNORE INTO Sofa (ID, Артикул , Доступность ) VALUES (?,?,?);"""
        data_tuple2 = (int(ID_item), int(article[article.find(":") + 1:]), item_available)
        cursor.execute(sqlite_insert_with_param1, data_tuple1)
        conn.commit()
        cursor.execute(sqlite_insert_with_param2, data_tuple2)
        conn.commit()

    Next_page = "" #отсчистили старое значение
    Next_page = soup.find('a', class_='page-link next')# ищем ссылку на следующую страницу
    if Next_page == None: # если ссылка на следующую страницу не имеется
        url = None
    else:# если нашли ссылку на следующую страницу
        Next_page = Next_page.get('href')
        newUrl = '/'.join(url.split('/')[:-1])             # обрезаем лишнее у старого url
        url = newUrl.replace('/catalog/0000057', Next_page)# меняем url на новый

#вывод в консоль
cursor.execute("""SELECT * from sofa left join vendor on vendor.Артикул = sofa.Артикул""")
rows = cursor.fetchall()
for row in rows:
    if row[2] != 'в пути':
        print("ID:", row[0])
        print("Артикул:", row[1])
        print("Название:", row[4])
        print("Доступность:", row[2])
        print("Цена без скидки:", row[5])
        if row[6] != 0:
            print("Цена со скидкой:", row[6], end="\n\n")
        else: print(end="\n\n")