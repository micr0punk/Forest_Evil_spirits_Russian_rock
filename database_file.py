import sqlite3


# with sqlite3.connect('data\\database_folder\\all_data.db') as db:
#     cursor = db.cursor()
#     cursor.execute('''SELECT * FROM characters_stats''',)
#     stats = cursor.fetchall()
#     for stat in stats:
#         #  print(stat)


def load_items_from_db():
    try:
        with sqlite3.connect('data\\database_folder\\all_data.db') as db:
            cursor = db.cursor()
            data = list(cursor.execute('''SELECT * FROM items''').fetchall())

            return data

    except Exception as e:
        print(e)
        print('Не удалось подключится к базе данных')
