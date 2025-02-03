import sqlite3
import csv
import chardet
import os


#  Добавление события в БД
def add_event_to_db(date_fr_f, event_fr_f, marker_fr_f, time_fr_f):
    try:
        with sqlite3.connect('database_folder/data_base_file.db') as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO events_table (date, event, marker, time) VALUES(?, ?, ?, ?)''',
                           (date_fr_f, event_fr_f, marker_fr_f, time_fr_f))
            db.commit()

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')

#  Изменение события в БД
def change_event_in_db(event, date_fr_f, event_fr_f, marker_fr_f, time_fr_f):
    try:
        with sqlite3.connect('database_folder/data_base_file.db') as db:
            cursor = db.cursor()
            cursor.execute('''UPDATE events_table SET date = ?, event = ?, marker = ?, time = ? WHERE event = ?''',
                           (date_fr_f, event_fr_f, marker_fr_f, time_fr_f, event))
            db.commit()

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')

#  Удаление события из БД
def delete_event_from_db(event_func, date_func, time_func):
    try:
        with sqlite3.connect('database_folder/data_base_file.db') as db:
            cursor = db.cursor()
            cursor.execute('''DELETE FROM events_table WHERE event = ? AND date = ? AND time = ?''',
                           (event_func, date_func, time_func))
            db.commit()

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')

#  Экспорт БД в CSV файл
def export_to_csv(directory):
    try:
        with sqlite3.connect('database_folder/data_base_file.db') as db:
            cursor = db.cursor()
            database = cursor.execute('''SELECT * FROM events_table''').fetchall()

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')

    try:
        with open(f'{directory}\\database_export_file.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL)

            writer.writerow(
                ['Дата', 'Событие', 'Метка', 'Время'])

            for i in range(len(database)):
                item = database[i]
                writer.writerow(list(item))

    except Exception as e:
        print(e)
        print('Не удалось записать базу данных в CSV файл')

#  Импорт в БД из CSV файла
def import_from_csv(file_name):
    try:
        with open(f'{file_name}', 'rb') as export_file:
            byte_data = export_file.read()
            encoding = chardet.detect(byte_data)['encoding']

    except Exception as e:
        print(e)
        print('Не удалось прочитать файл')

    try:
        with open(f'{file_name}', 'r', encoding=encoding) as export_file:
            reader = csv.reader(export_file, delimiter=';', quotechar='"')
            with open(f'programfiles\\temporary.csv', 'w', newline='', encoding="utf-8") as temporary_file:
                writer = csv.writer(temporary_file, delimiter=';', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    writer.writerow(row)

    except Exception as e:
        print(e)
        print('Не удалось записать временный файл')

    try:
        with open(f'programfiles\\temporary.csv', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')

            with sqlite3.connect('database_folder/data_base_file.db') as db:
                cursor = db.cursor()
                for row in reader:
                    if row != ['Дата', 'Событие', 'Метка', 'Время']:
                        cursor.execute('''INSERT INTO events_table (date, event, marker, time) VALUES(?, ?, ?, ?)''',
                                       (row[0], row[1], row[2], row[3]))
                db.commit()

    except Exception as e:
        print(e)
        print('Не удалось прочитать файл/подключиться к базе данных')

    try:
        os.remove(f'programfiles\\temporary.csv')

    except Exception as e:
        print(e)
        print('Не удалось удалить временный файл')

#  Полная очистка БД
def delete_all_from_db():
    try:
        with sqlite3.connect('database_folder/data_base_file.db') as db:
            cursor = db.cursor()
            cursor.execute('''DELETE FROM events_table''')
            db.commit()

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')
