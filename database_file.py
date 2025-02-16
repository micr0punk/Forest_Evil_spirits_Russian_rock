import sqlite3


def load_items_from_db():
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM items''').fetchall())

            data_output = {'50': data[0],
                           '51': data[1],
                           '52': data[2],
                           '53': data[3],
                           '70': data[4],
                           '71': data[5],
                           '72': data[6],
                           '73': data[7],
                           '74': data[8],
                           '75': data[9],
                           '76': data[10],
                           }

            return data_output

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')


def load_character_from_db(idd):
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM characters_stats WHERE id = ?''', (idd,)).fetchall())

            return data

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')


def load_enemies_from_db():
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM enemies_stats''').fetchall())

            data_output = {'40': data[0],
                           '41': data[1],
                           '42': data[2],
                           '43': data[3],
                           }

            return data_output

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')


def load_allies_from_db(excluded_character):
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM characters_stats''').fetchall())

            data_output = {'31': data[0] if excluded_character != 'Маг' else None,
                           '32': data[0] if excluded_character != 'Лесник' else None,
                           '33': data[0] if excluded_character != 'Шут' else None,
                           '34': data[0] if excluded_character != 'Анархист' else None
                           }

            return data_output

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')
