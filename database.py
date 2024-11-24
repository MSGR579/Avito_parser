import sqlite3
from datetime import datetime

class Database:
    """
    Класс, в котором  реализованы методы для добавления данных в хеш. DDL, DML, DQL команды.

    """

    def __init__(self):
        self.connection = sqlite3.connect("cache.db")
        self.cursor = self.connection.cursor()
        self.DDL_commands()
        
    def DDL_commands(self):
        #Создание таблицы
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id TEXT PRIMARY KEY,
                search_query TEXT,
                price TEXT,
                description TEXT,
                name TEXT,
                link TEXT,
                city TEXT,
                images TEXT,
                address TEXT,
                date TEXT,
                views TEXT,
                status TEXT,
                added_time TIMESTAMP,
                last_updated TIMESTAMP
            )
        ''')
        self.connection.commit()

    def DML_commands(self, listing):
        #получение текущего времени
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            SELECT * FROM listings WHERE id = ?
        ''', (listing['id'],))
        existing_listing = self.cursor.fetchone()

        if existing_listing is None:
            
            # если статус закрыто, то не добавляем запись
            if listing['status'] == 'закрыто':
                return

            listing['added_time'] = current_time
            listing['last_updated'] = current_time

            # Добавление данных в таблицу БД
            self.cursor.execute('''
                INSERT INTO listings (id, search_query, price, description, name, link, city, images, address, date, views, status, added_time, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?)
            ''', (listing['id'], listing['search_query'], listing['price'], listing['description'], listing['name'],
                  listing['link'],listing['city'], listing['images'], listing['address'], listing['date'], listing['views'], listing['status'],
                  listing['added_time'], listing['last_updated']))
        else:
            #Проверка на то, изменились ли кэшируемые данные или нет
            changes = False
            if existing_listing[2] != listing['price']:
                changes = True
            if existing_listing[3] != listing['description']:
                changes = True
            if existing_listing[4] != listing['name']:
                changes = True
            if existing_listing[11] != listing['status']:
                changes = True
            
            if changes:
                self.cursor.execute('''
                    UPDATE listings SET price=?, description=?, name=?, last_updated=?,
                    status=? WHERE id=?
                ''', (listing['price'], listing['description'], listing['name'],
                      current_time, listing['status'], listing['id']))

        self.connection.commit()

    def close(self):
        self.connection.close()