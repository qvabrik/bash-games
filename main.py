import menu
import database
import team

db = database.Database()
menu = menu.Menu()
tm = team.Team()

# проверяем БД, если её нет - создаём
db.DatabaseCheck()
menu.Hello()
#проверяем есть ли значения в БД, если нет - сразу создаём новую команду
isEmpty = db.TableCheck()
if isEmpty == True:
    print('\nОго, это ваш первый запуск? Нужно создать команду!')
    tm.New()
#запускаем главное меню
menu.Navigation()


exit()