import pymysql.cursors


class SQL:
    def __init__(self, dbhost, db, dbpassword):
        """Подключение к БД"""
        self.cur = None
        self.host = dbhost
        self.user = "root"
        self.password = "1111"
        self.database = db
        self.charset = "utf8"
        self.port = 3306
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        self.create_table_config()
        self.create_table_database()

    def connect(self):
        connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset,
            port=self.port)
        return connection

    def create_table_config(self):
        """Создание таблицы для хранения каналов"""
        self.cur = self.connection.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS config(donor varchar(255), moder varchar("
                         "255), channel varchar(255))")
        return self.connection.commit()

    def create_table_database(self):
        """Создание таблицы для хранения информации о постах"""
        self.cur = self.connection.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS DataBase1(id MEDIUMINT UNSIGNED ZEROFILL AUTO_INCREMENT, username "
                 "varchar(255), message_id varchar(255), PRIMARY KEY (id))")
        return self.connection.commit()

    def message_id_exists(self, username, message_id: int):
        """Проверка есть ли message_id в БД"""
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT * FROM DataBase1 WHERE username=%s AND message_id=%s", (username, message_id,))
        result = self.cur.fetchall()
        return bool(len(result))

    def add_message_id(self, username, message_id):
        """Добавление message_id"""
        self.cur = self.connection.cursor()
        self.cur.execute("INSERT INTO DataBase1 VALUES (NULL,%s,%s)", (username, message_id,))
        return self.connection.commit()

    def get_last_rowid(self):
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT COUNT(*) FROM DataBase1")
        result = self.cur.fetchone()
        num = int(result[0])-1
        self.cur.execute("SELECT id FROM DataBase1 LIMIT 1 OFFSET %s", (num,))
        return self.cur.fetchone()

    def get_data_in_table(self, message):
        """Получение записи о посте в таблице"""
        self.cur = self.connection.cursor()
        self.cur.execute(f"SELECT * FROM DataBase1 WHERE id = {message.text}")
        return self.cur.fetchone()

    def add_donor(self, name: str):
        """Добавление канала донора"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT donor FROM config WHERE donor=%s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            self.cur.execute("INSERT INTO config (donor) VALUES (%s)", (name,))
            self.connection.commit()
            return f'Запись {name} добавлена.'
        return f'Запись {name} существует.'

    def delete_donor(self, name: str):
        """Удаление канала донора"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT donor FROM config WHERE donor = %s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            return f'Запись {name} не найдена.'
        else:
            self.cur.execute("DELETE FROM config WHERE donor = %s", (name,))
            self.connection.commit()
            return f'Запись {name} удалена.'

    def add_moder(self, name: str):
        """Добавление канала модерации"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT moder FROM config WHERE moder=%s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            self.cur.execute("INSERT INTO config (moder) VALUES (%s)", (name,))
            self.connection.commit()
            return f'Запись {name} добавлена.'
        return f'Запись {name} существует.'

    def delete_moder(self, name: str):
        """Удаление модера"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT moder FROM config WHERE moder = %s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            return f'Запись {name} не найдена.'
        else:
            self.cur.execute("DELETE FROM config WHERE moder = %s", (name,))
            self.connection.commit()
            return f'Запись {name} удалена.'

    def add_channel(self, name: str):
        """Добавление основного канала"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT channel FROM config WHERE channel=%s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            self.cur.execute("INSERT INTO config (channel) VALUES (%s)", (name,))
            self.connection.commit()
            return f'Запись {name} добавлена.'
        return f'Запись {name} существует.'

    def delete_channel(self, name: str):
        """Удаление основного канала"""
        # Проверка на наличие записи такого канала
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT channel FROM config WHERE channel = %s", (name,))
        result = self.cur.fetchall()
        if not bool(len(result)):
            return f'Запись {name} не найдена.'
        else:
            self.cur.execute("DELETE FROM config WHERE channel = %s", (name,))
            self.connection.commit()
            return f'Запись {name} удалена.'

    def get_donor(self):
        """Возвращает список с каналами донорами"""
        self.cur = self.connection.cursor()
        donor_list = []
        self.cur.execute("SELECT donor FROM config")
        result = self.cur.fetchall()
        for donor in result:
            if donor[0] is None:
                pass
            else:
                donor_list.append(donor[0])
        return donor_list

    def get_moder(self):
        """Возвращает канал модерации"""
        self.cur = self.connection.cursor()
        moder = None
        self.cur.execute("SELECT moder FROM config")
        result = self.cur.fetchall()
        for i in result:
            if i[0] is None:
                pass
            else:
                moder = i[0]
        return moder

    def get_channel(self):
        """Возвращает основной канал"""
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT channel FROM config")
        result = self.cur.fetchall()
        for i in result:
            if i[0] is None:
                pass
            else:
                channel = i[0]
        return channel

    def print_donor(self):
        """Возвращает список каналов доноров"""
        self.cur = self.connection.cursor()
        donor_list = []
        self.cur.execute("SELECT donor FROM config")
        result = self.cur.fetchall()
        for donor in result:
            donor_list.append(donor[0])
        return donor_list

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

