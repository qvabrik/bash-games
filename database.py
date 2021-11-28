import os.path
import sqlite3 as sql

class Database:

    #подключаемся к БД и создаём курсор
    def DatabaseOpen(self):
        self.connection = sql.connect('database.sqlite3')
        self.q = self.connection.cursor()

    #закрываем БД
    def DatabaseClose(self):
        self.q.close()
        self.connection.close()

    #проверяем существование БД, если её нет - создаём
    def DatabaseCheck(self):
        if os.path.exists('database.sqlite3') == False:
            self.DatabaseOpen()
            #создаём БД
            self.q.execute('''CREATE TABLE `players` (`id` INT AUTO_INCREMENT, `name` VARCHAR(30), `balance` INT(5), PRIMARY KEY(id))''')
            self.connection.commit()
            self.DatabaseClose()

    def TableCheck(self):
        self.DatabaseOpen()
        isEmpty = False
        info = self.q.execute("""SELECT * FROM `players` WHERE `id`=1""")
        if info.fetchone() == None:
            isEmpty = True
        return isEmpty

    #очищаем БД для создания новой команды
    def DatabaseClear(self):
        self.DatabaseOpen()
        self.q.execute('''DELETE FROM `players`''')
        self.connection.commit()
        self.DatabaseClose()

    #ID разметка новой команды от количества игроков
    def DatabaseAddID(self, quantity):
        self.DatabaseOpen()
        i = 1
        while i <= quantity:
            request = """INSERT INTO `players` (id, `name`, `balance`) VALUES (?, 'Default', 0)"""
            self.q.execute(request, str(i))
            self.connection.commit()
            i += 1
        self.DatabaseClose()

    #Добавление имен в БД
    def DatabaseAddNames(self, dist):
        self.DatabaseOpen()
        i = 1
        while i <= len(dist):
            name = dist[i]['name']
            request = """UPDATE `players` SET name = ? WHERE `id` = ?"""
            self.q.execute(request, (name, str(i)))
            self.connection.commit()
            i += 1
        self.DatabaseClose()

    # Синхронизация баланса В БД
    def DatabaseAddBalance(self, dist):
        self.DatabaseOpen()
        i = 1
        while i <= len(dist):
            balance = dist[i]['balance']
            request = """UPDATE `players` SET balance = ? WHERE `id` = ?"""
            self.q.execute(request, (balance, str(i)))
            self.connection.commit()
            i += 1
        self.DatabaseClose()

    # Синхронизация таблицы ИЗ БД
    def DatabaseGet(self):
        self.DatabaseOpen()
        dist = {}
        request = """SELECT * from `players`"""
        self.q.execute(request)
        records = self.q.fetchall()
        for i in records:
            dist[i[0]] = {'name': i[1], 'balance': i[2]}
        return dist
        self.DatabaseClose()