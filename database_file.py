import sqlite3


def load_items_from_db():
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM items''').fetchall())

            return data

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')


def load_character_from_db(id):
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM characters_stats WHERE id = ?''', (id,)).fetchall())

            return data

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')
