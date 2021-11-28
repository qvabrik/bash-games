import database
import team
import random
import time
from datetime import datetime, date

db = database.Database()
tm = team.Team()

class FindACard:
    def Game(self):
        #проверим, что игроков с положительным балансом > 1
        check = self.IsPlayersOne()
        if check == False:
            self.GameScheme()
        elif check == True:
                print('В текущей команде только один игрок с положительным балансом! Чтобы пополнить баланс или создать новую команду, перейдите в настройки.')

    def GameScheme(self):
        activeTeam = self.ActiveTeamCreate()
        print('\nНачнём! Цель игры - среди нескольких карт с палочками [ -- ] найти единственную карту с крестиками [ XХ ]')
        # объявляем участников и их балансы
        print('В этой игре участвуют: ', end='')
        ids = list(activeTeam.keys())
        print(activeTeam)
        for i in ids:
            name = activeTeam[i]['name']
            balance = activeTeam[i]['balance']
            print('-- ' + str(name) + ', баланс: ' + str(balance) + ' рублей.')

        # игроки делают ставки
        # определяем минимальный баланс
        maxBet = self.maxBet(activeTeam)
        print('\nУчастники, делайте ставку!')
        print('-выбранная ставка спишется со счёта каждого из игроков\n-максимальная ставка этого раунда составляет: '  + str(maxBet) + ' м.')
        bet = self.Bet(maxBet)
        # уменьшаем балансы игроков
        for i in activeTeam:
            activeTeam[i]['balance'] -= bet
        prize = bet * len(activeTeam)
        wordEnd = tm.WordEndCheck(prize)
        print('ПРИЗОВОЙ ФОНД этого раунда составит ' + str(prize) + ' монет' + wordEnd + '!')

        # готовим игру
        # создаём массив карт
        cardsQuantity = self.CardsQuantity(activeTeam)
        cardsArray = self.CardsArray(cardsQuantity)
        # определяем индекс выигрышной карту
        winCard = random.randint(0, (cardsQuantity - 1))
        # определяем ID игрока, который начнёт
        firstPlayer = ids[(random.randint(0, (len(ids) - 1)))]

        # игра
        print('Начнём игру!')
        winnerID = self.GameEngine(ids, activeTeam, cardsArray, winCard, firstPlayer)
        # добавим приз победителю
        activeTeam[winnerID]['balance'] += prize

        # синхронизация
        # запишем балансы из activeTeam в полный массив
        team = db.DatabaseGet()
        for i in ids:
            team[i]['balance'] = activeTeam[i]['balance']
        # передадим полный массив в БД
        db.DatabaseAddBalance(team)


    def ActiveTeamCreate(self):
        # team = {1: {'name': 'Keereal', 'balance': 300}, 2: {'name': 'Rita', 'balance': 91}, 3: {'name': 'Looser', 'balance': 0}, 4: {'name': 'Stepik', 'balance': 998}}
        team = db.DatabaseGet()
        activeTeam = {}
        for i in team:
            if team[i]['balance'] != 0:
                activeTeam[i] = team[i]
        return activeTeam

    def maxBet(self, dist):
        minBet = 1000
        for i in dist:
            if dist[i]['balance'] < minBet:
                minBet = dist[i]['balance']
        return minBet

    def Bet(self, maxBet):
        bet = 0
        while True:
            try:
                bet = int(input('Ставка раунда: '))
                if bet > maxBet:
                    print('Ставка не может быть больше ' + str(maxBet) + '. Попробуйте ещё раз!')
                    continue
                elif bet == 0:
                    print('Ставка не может быть равной 0. Попробуйте ещё раз!')
                    continue
                elif bet < 0:
                    print('Ставка не может быть отрицательной. Попробуйте ещё раз!')
                    continue
                break
            except ValueError:
                print('Ставка не может быть выражена таким образом! Попробуйте ещё раз.')
                continue
        return bet

    def CardsQuantity(self, dist):
        cardsQuantity = 0
        teamQuantity = len(dist)
        while True:
            try:
                cardsQuantity = int(input('Выберите количество карт от ' + str(teamQuantity) + ' до ' + str(teamQuantity * 3) + ': '))
                if cardsQuantity > (teamQuantity * 3):
                    print('Количество карт не должно быть больше ' + str(teamQuantity * 3) + '. Попробуйте ещё раз!')
                    continue
                elif cardsQuantity < teamQuantity:
                    print('Количество карт не должно быть меньше ' + str(teamQuantity) + '. Попробуйте ещё раз!')
                    continue
                break
            except ValueError:
                print('Количество карт не может быть выражена таким образом! Попробуйте ещё раз.')
                continue
        return cardsQuantity

    def CardsArray(self, quantity):
        cards = []
        i = 1
        while i <= quantity:
            card = '[ ' + str(i) + ' ]'
            cards.append(card)
            i += 1
        return cards

    def GameEngine(self, ids, activeTeam, cardsArray, winCard, firstPlayer):
        i = ids.index(firstPlayer)
        while True:
            playerID = ids[i]
            player = activeTeam[playerID]['name']
            print('Карты на столе: ', end='')
            for ex in cardsArray:
                print(ex, end='   ')
            print('')
            print('\nХодит игрок ' + player + '. ', end='')
            while True:
                try:
                    playerChoice = int(input('Выберите карту: ')) - 1
                    if (playerChoice < 0) or (playerChoice > (len(cardsArray) - 1)):
                        print('На столе нет такой карты! Попробуйте ещё раз.')
                        continue
                    elif cardsArray[playerChoice] == '[ -- ]':
                        print('Эта карта уже открыта! Попробуйте ещё раз.')
                        continue
                    elif playerChoice != winCard:
                        print('Не угадали!')
                        cardsArray[playerChoice] = '[ -- ]'
                        break
                    elif playerChoice == winCard:
                        # тянем время
                        t = 0
                        while t < 4:
                            print('...')
                            time.sleep(0.5)
                            t += 1
                        # выводим карты
                        print('Карты на столе: ', end='')
                        cardsArray[playerChoice] = '[ XX ]'
                        for ex in cardsArray:
                            print(ex, end='   ')
                        print('')
                        # поздравляем победителя
                        print('Правильный выбор! Побеждает игрок ' + player + '!!!')
                        return playerID
                        break
                except ValueError:
                    print('Номер карты не может быть выражен подобным образом! Попробуйте ещё раз.')
                    continue
            i += 1
            if i == len(ids):
                i = 0

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
