import time
from datetime import datetime, date
import team
import database
import findACard

db = database.Database()
tm = team.Team()
gameFindACard = findACard.FindACard()

class Menu:

    # Приветсвие!
    def Hello(self):
        i = 0
        print('protocol initialization', end='')
        while i < 4:
            print('.', end='')
            time.sleep(0.5)
            i += 1
        print('\nДобро пожаловать в коллекцию многопользовательских игр для терминала!')
        # посчитаем разницу в месяцах между датой разработки и сегодняшней датой
        creating_date = date(2021, 12, 1)
        current_date = datetime.now().date()
        diff = abs((current_date - creating_date).days)
        print('Коллекция разработана в декабре 2021, ' + str(diff) + ' дней тому назад!')

    # Навигация
    def Navigation(self):
        while True:
            command = input('\n-->Главное меню. Введите команду: ')
            if command == "игра":
                #проверка что игроков с положительным балансом > 1
                isPlayerOne = self.IsPlayersOne()
                if isPlayerOne == True:
                    print('В текущей команде только один игрок с положительным балансом! Чтобы пополнить баланс или создать новую команду, перейдите в настройки.')
                    continue
                self.Game()
                continue
            elif command == "настройки":
                self.Setting()
                continue
            elif command == "помощь":
                print('Список доступных команд:\n[игра] - выбрать игру\n[настройки] - настройки команды\n[помощь] - справка\n[выход] - выйти из игры')
                continue
            elif command == "выход":
                break
            else:
                print('Упс! Нет такой команды. Для помощи введите [помощь]')

    def Game(self):
        while True:
            command = input('\n-->Выберите игру: ')
            if command == 'найди карту':
                gameFindACard.Game()
                continue
            elif command == 'помощь':
                print('Пока что доступна только одна игра:\nНайди карту [найди карту]')
                continue
            elif command == 'назад':
                break
            else:
                print('Нет такой игры! Для помощи введите [помощь]')
                continue

    def Setting(self):
        while True:
            command = input('\n-->Настройки игроков. Введите команду: ')
            if command == "команда":
                team = db.DatabaseGet()
                i = 1
                while i <= len(team):
                    name = team[i]['name']
                    balance = team[i]['balance']
                    print('Игрок №' + str(i) + ', зовут: ' + str(name) + '. Баланс: ' + str(balance) + ' рублей.')
                    i += 1
                continue
            elif command == "баланс":
                tm.ChangeBalance()
                continue
            elif command == "новая":
                while True:
                    command = input('Создание новой команды приведёт к потере предыдущей. Вы уверены? [да]/[нет]: ')
                    if command == 'да':
                        tm.New()
                        break
                    elif command == 'нет':
                        break
                    else:
                        print('Выберите [да] или [нет]')
                        continue
                continue
            elif command == "помощь":
                print('Список доступных команд:\n[команда] - показать текущую команду и балансы игроков\n[баланс] - сбросить или пополнить баланс\n[новая] - создвть новую команду\n[помощь] - справка\n[назад] - назад в главное меню')
                continue
            elif command == "назад":
                break
            else:
                print('Упс! Нет такой команды. Для помощи введите [помощь]')

    def IsPlayersOne(self):
        team = db.DatabaseGet()
        isPlayerOne = False
        check = 0
        for i in team:
            if team[i]['balance'] > 0:
                check += 1
        if check <= 1:
            isPlayerOne = True
        return isPlayerOne

