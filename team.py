import database

db = database.Database()

#класс Команда
class Team:

    teamQuantity = 0
    teamNames = {}

    #конструктор переменных по умолчанию
    # def __init__(self):
    #     self.teamNames = db.DatabaseGet()


    # функция выбора количества игроков
    def TeamQuantity(self):
        while True:
            try:
                self.teamQuantity = int(input('Введите количество игроков: '))
                if self.teamQuantity == 1:
                    print('Позовите хотя бы воображаемого друга! Попробуйте ещё раз.')
                    continue
                elif self.teamQuantity < 1:
                    print('Ну и как вы собрались играть? Попробуйте ещё раз.')
                    continue
                elif self.teamQuantity > 5:
                    print('Не обманывайте себя - откуда у вас столько друзей? Укажите число друзей не более 5. Попробуйте ещё раз.')
                    continue
                break
            except ValueError:
                print('Число игроков не может быть выражено таким образом! Попробуйте ещё раз.')
                continue
        # создаём строки с ID в БД
        db.DatabaseAddID(self.teamQuantity)
        return self.teamQuantity

    # функция "знакомства" с игроками, которая создаёт словарь вида {n: {'name': '...', 'balance' = '...'}, ...}
    def TeamNames(self):
        i = 0
        while i < self.teamQuantity:
            name = str(input('Введите имя игрока #' + str(i + 1) + ': '))
            self.teamNames[i + 1] = {'name': name, 'balance': 0}
            i += 1
        # передаём имена в БД
        db.DatabaseAddNames(self.teamNames)
        return self.teamNames

    #установим балансы для всей команды: по умолчанию всем по 100 монет, либо же каждому игроку индивидуальное количество
    def TeamSetBalance(self):
        print('Теперь необходимо пополнить счёт игроков!')
        print('Введите команду [стандарт], чтобы установить баланс каждого игрока равный 100 рублям.')
        print('Введите команду [индивид], чтобы установить свой баланс для каждого игрока.')
        while True:
            command = input(str('Введите команду: '))
            if command == 'стандарт':
                i = 1
                while i <= len(self.teamNames):
                    self.teamNames[i]['balance'] = 100
                    i += 1
                break
            elif command == 'индивид':
                i = 1
                while i <= len(self.teamNames):
                    self.PlayerAddBalance(i)
                    i += 1
                break
            else:
                print('Выберите команду [стандарт] или [индивид].')
                continue
        # передадим балансы в БД
        db.DatabaseAddBalance(self.teamNames)

    #поиск ID игрока
    def PlayerIDSearching(self, name):
        id = 0
        for i in self.teamNames:
            if self.teamNames[i]['name'] == name:
                id = i
        return id

    #установить баланс игрока
    def PlayerAddBalance(self, id):
        name = self.teamNames[id]['name']
        while True:
            try:
                # подгрузим БД для проверки балансов, не будем делать баланс больше 1000
                team = db.DatabaseGet()
                balance = int(input('Укажите, сколько монет добавить игроку ' + name + ': '))
                if balance < 0:
                    print('Количество монет не может быть меньше нуля. Попробуйте ещё раз.')
                    continue
                elif (balance + int(team[id]['balance']) > 1000):
                    dif = 1000 - int(team[id]['balance'])
                    wordEnd = self.WordEndCheck(dif)
                    print('Баланс игрока не может быть больше 1000 монет! Вы можете добавить максимум ' + str(dif) + ' монет' + wordEnd + '.')
                    continue
                self.teamNames[id]['balance'] += balance
                break
            except ValueError:
                print('Количество монет может быть выражено только целым числом. Попробуйте ещё раз.')
                continue

    #функция "приветствия" игроков
    def Greeting(self):
        i = 1
        print('Добро пожаловать в игру,', end=' ')
        while i <= (len(self.teamNames) - 1):
            print(self.teamNames[i]['name'] + ", ", end='')
            i += 1
        print(self.teamNames[i]['name'] + "!")

    # функция проверки окончания слова МОНЕТ в формулировках типа "добавить Х монет"
    def WordEndCheck(self, number):
        wordEnd = ''
        temp = []
        for i in str(number):
            temp.append(i)
        if temp[-1] == '1':
            wordEnd = 'у'
        elif temp[-1] == '2' or temp[-1] == '3' or temp[-1] == '3':
            wordEnd = 'ы'
        return wordEnd

    # создать новую команду
    def New(self):
        db.DatabaseClear()
        self.teamNames = {}
        self.TeamQuantity()
        self.TeamNames()
        self.Greeting()
        self.TeamSetBalance()
        db.DatabaseAddBalance(self.teamNames)

    # меню добавления монет отдельному игроку на выбор
    def ChangeBalance(self):
        team = db.DatabaseGet()
        while True:
            try:
                name = input('Введите имя игрока, которому необходимо пополнить баланс (или [выход] для возврата в настройки): ')
                if name == 'выход':
                    break
                else:
                    id = self.PlayerIDSearching(name)
                if team[id]['balance'] == 1000:
                    print('Этот игрок уже имеет максимальный баланс!')
                    break
                if id == 0:
                    print('Нет такого игрока! Попробуйте ещё раз.')
                    continue
                else:
                    self.PlayerAddBalance(id)
                db.DatabaseAddBalance(self.teamNames)
                break
            except ValueError:
                print('Неверная команда. Попробуйте ещё раз.')
                continue