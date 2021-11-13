#********************************************************
# ФГБОУ ВО "НИУ "МЭИ""                                  *
# Институт информационных и вычислительных технологий   *
# Кафедра Управления и интеллектуальных технологий      *
#                                                       *
# Научно-исследовательская работа по теме               *
# "Основы работы с базами данных"                       *
#                                                       *
# Выполнил: студент группы А-03-19                      *
#           Баснак Е.А.                                 *
# Проверил: Фомин Г.А.                                  *
#********************************************************


import sqlite3
import sys
import time
import os
os.chdir('C:\\PO_AS\\NIR\\part2')


# Название таблицы
tblname = 'stud'

### Создание БД
def dbCreate(dbName):
    """Создание БД
Входной аргумент: имя БД
В результате работы функции в рабочем каталоге создаётся файл БД с указанным именем"""
    
    # Создание файла БД
    con = sqlite3.connect(dbName)

    # Создание курсора
    cur = con.cursor()

    # Формирование SQL-запроса
    sql = """\
    CREATE TABLE stud (code TEXT,
    subject TEXT,
    sem_number INTEGER,
    type_of_cert TEXT,
    date_of_cert DATE,
    prof_fio TEXT,
    prof_pos TEXT,
    mark INTEGER,
    date_of_update DATE);
    """

    # Выполнение запроса
    cur.executescript(sql)

    # Закрытие БД
    cur.close()
    con.close()


def frontSpaceDel(strk):
    """Удаление пробелов в начале строки
Входной аргумент: строка, из которой надо удалить начальные пробелы
Возвращаемый результат функции: исходная строка без начальных пробелов"""
    
    # Удаление начальных пробелов
    for ch in strk:
        if (ch == ' '):
            strk = strk[1:]
        if (ch.isalpha() or ch == '_'):
            break
    return strk


def backSpaceDel(strk):
    """Удаление пробелов в конце строки
Входной аргумент: строка, из которой надо удалить конечные пробелы
Возвращаемый результат функции: исходная строка без конечных пробелов"""
    
    # Удаление заключительных пробелов
    for ch in reversed(strk):
        if (ch == ' '):
            strk = strk[:-1]
        if (ch.isalpha() or ch == '_'):
            break
    return strk


def fullSpaceDel(strk):
    """Удаление пробелов в начале и конце строки
Входной аргумент: строка, из которой надо удалить начальные и конечные пробелы
Возвращаемый результат функции: исходная строка без начальных и конечных пробелов"""
    
    strk = frontSpaceDel(strk)
    strk = backSpaceDel(strk)
    return strk

def showFields(fields):
    """Вывод имен указанных полей на экран
Входной аргумент: список имен полей для вывода
В результате работы функции на экран выводится заголовок таблицы БД"""
    
    print('{:^10} | {:^30} | {:^10} | {:^12} | {:^12} | {:^30} | {:^15} | {:^4} | {:^15}'.format(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]))
    for i in range(23): # В сумме 161
        print('-------', end = '')
    print('')


def showData(data):
    """Вывод содержимого таблицы БД на экран
Входной аргумент: список, состоящий из списков - строк таблицы БД
В результате работы функции на экран выводится содержимое таблицы БД"""
    
    for di in data:
        print('{:^10} | {:^30} | {:^10} | {:^12} | {:^12} | {:^30} | {:^15} | {:^4} | {:^15}'.format(di[0], di[1], di[2], di[3], di[4], di[5], di[6], di[7], di[8]))
    
    print('')


def menu():
    """Вывод меню и выбор действия
Возвращаемый результат функции: выбранное пользователем действие"""
    
    print('')
    print('Меню:')
    print('1) Отображение текущуго содержимого БД на экране в виде таблицы.')
    print('2) Сохранение таблицы в текстовый файл с задаваемым именем.')
    print('3) Добавление строки в БД')
    print('4) Задание условия отбора.')
    print('0) Завершение работы с программой.')
    res = input('Выберите действие: ')
    
    # Удаление пробелов в начале и конце строки
    res = fullSpaceDel(res)
    
    print('')
    return res


def subMenu():
    """Вывод второго уровня меню и выбор действия
Возвращаемый результат функции: выбранное пользователеме действие в данном меню"""
    
    print('')
    print('Задание условия отбора')
    print('1) Ввод условия')
    print('2) Просмотр подмножества')
    print('3) Замена значений подмножества')
    print('4) Удаление подмножества')
    print('0) Вернуться в главное меню')
    res = input('Выберите действие: ')

    # Удаление пробелов в начале и конце строки
    res = fullSpaceDel(res)
    
    print('')
    return res


def fieldNames(dbName):
    """Получение списка имен полей
Входной аргумент: имя БД
Возвращаемый результат функции: список, содержащий имена полей указанной БД"""
    
    # Открытие БД
    con = sqlite3.connect(dbName)
          
    # Создание курсора
    cur = con.cursor()
    
    # Формирование строки с SQL-запросомом
    sql = """\
SELECT * FROM {}""".format(tblname)
    
    # Исполнение запроса
    cur.execute(sql)
    
    # Запись имен полей
    fields = cur.description
    
    # Закрытие БД
    cur.close()
    con.close()
    
    # Извлечение имен полей из кортежа
    return [nam[0] for nam in fields]


def dbData(dbName):
    """Получение списка содержимого таблицы БД
Входной аргумент: имя БД
Возвращаемый результат функции: список, содержащий списки-строки таблицы БД"""
    
    # Открытие БД
    con = sqlite3.connect(dbName)
    
    #Создание курсора
    cur = con.cursor()

    # Получание содержимого таблицы
    sql = 'SELECT * FROM {}'.format(tblname)
    data = cur.execute(sql).fetchall()

    # Закрытие БД
    cur.close()
    con.close()

    return data


def tableDisplay(dbName):
    """Вывод таблицы БД
Входной аргумент: имя БД
В результате работы функции на экран выводится таблица БД"""
    
    fields = fieldNames(dbName) # получение имен полей
    data = dbData(dbName) # получение содержимого таблицы

    showFields(fields) # вывод полей
    showData(data) # вывод содержимого

    

def tableFile(dbName):
    """Сохранение таблицы БД в файл
Входной аргумент: имя БД
В результате работы функции в рабочем каталоге создаётся или изменяется файл с указанным именем, в который записывается таблица БД"""
    
    # Ввод имени файла
    fileName = input('Введите имя файла для вывода:')
    
    # Запись текущего потока вывода
    vr_out = sys.stdout

    # Открытие файла вывода
    fc = open(fileName, 'w')

    # Перенацеливание стандартного потока вывода на файл
    sys.stdout = fc

    # Вывод таблицы
    tableDisplay(dbName)

    # Восстановление текущего потока
    sys.stdout = vr_out

    # Закрытие файла
    fc.close()

    print('Таблица записана в файл.')
    

def addRow(dbName):
    """Добавление строки в БД
Входной аргумент: имя БД
В результате работы функции в таблицу указнной БД добавляется новая строка"""
    
    # Ввод необходимых полей
    code = input('Введите код дисциплины по учебному плану: ')
    code = fullSpaceDel(code)
    
    subject = input('Введите название дисциплины: ')
    subject = fullSpaceDel(subject)
    
    sem_number = int(input('Введите номер семестра с аттестацией по дисциплине: '))
    
    type_of_cert = input('Введите тип аттестации (экзамен/зачет): ')
    type_of_cert = fullSpaceDel(type_of_cert)
    
    date_of_cert = input('Введите дату аттестации (в формате ДД-ММ-ГГГГ): ')
    date_of_cert = fullSpaceDel(date_of_cert)
    
    prof_fio = input('Введите ФИО преподавателя, проводившего аттестацию: ')
    prof_fio = fullSpaceDel(prof_fio)
    
    prof_pos = input('Введите должность преподавателя: ')
    prof_pos = fullSpaceDel(prof_pos)

    while True:
        mark = int(input('Введите полученную оценку: '))

        if (mark < 0 or mark > 5):
            print('Неверная оценка! Оценка должна находиться в диапазоне от 0 до 5!')
        else:
            break
    
    # Получение даты занесения записи
    dat = time.localtime()
    date_of_update = '{:0>2}-{:0>2}-{:0>4}'.format(str(dat.tm_mday), str(dat.tm_mon), str(dat.tm_year))

    # Создание кортежа с данными для занесения в таблицу
    new_data = (code, subject, sem_number, type_of_cert, date_of_cert, prof_fio, prof_pos, mark, date_of_update)

    # Открытие БД
    con = sqlite3.connect(dbName)

    # Создание курсора
    cur = con.cursor()

    # Формирование строки с SQL-запросом
    sql = """\
INSERT INTO {} 
(code, subject, sem_number, type_of_cert, date_of_cert, prof_fio, prof_pos, mark, date_of_update) 
VALUES (?,?,?,?,?,?,?,?,?)
""".format(tblname)

    # Занесение полученного кортежа в таблицу
    cur.execute(sql, new_data)

    # Сохранение изменений
    con.commit()

    # Закрытие БД
    cur.close()
    con.close()


def checkField(dbName, str_field):
    """Проверека введенного имени поля на соответствие полям таблицы
Входные аргументы: имя БД; имя поля для проверки
Возвращаемый результат функции: значение True, если указанное поле имеется в таблице иначе значение False"""
    
    # Удаление начальных пробелов (подготовка к проверке на соответствие поля)
    str_field = fullSpaceDel(str_field)
            
    # Получение имен полей таблицы
    right_fields = fieldNames(dbName)
    
    # Выделение имени поля из условия
    field = ''
    for ch in str_field:
        if (ch.isalpha() or ch == '_'):
            field = field + ch
        else:
            break

    return field in right_fields #True если принадлежит
    

def condEnter(dbName):
    """Ввод условия отброа подмножества
Входной аргумент: имя БД
Возвращаемый результат функции: строка, содержащая условие отбора подмножества таблицы БД"""
    
    while True:
        # Ввод условия
        res = input('Введите условие для отбора подмножества: ')

        # Проверка имени поля из условия
        if checkField(dbName, res):
            break
        
        else:
            print('Несуществующее поле БД! Попробуйте еще раз.')


    print('Условие сохранено')
    
    return res


def showSubTable(dbName, cond):
    """ Отображение подмножества строк, удовлетворяющих заданному условию
Входные аргументы: имя БД; условие для отбора подмножества строк таблицы
В результате работы функции на экран будет выведена шапка таблицы и подмножество строк, удволетворяющих заданному условию"""
    
    # Проверка наличия условия
    if (cond == ''):
        print('Условие отсутствует! Введите условие и повторите попытку.')
        return

    # Открытие БД
    con = sqlite3.connect(dbName)
    cur = con.cursor()

    # Создание SQL-запроса
    sql = 'SELECT * FROM {0} WHERE {1}'.format(tblname, cond)

    # Получение данных из таблицы
    data = cur.execute(sql).fetchall()

    # Закрытие БД
    cur.close()
    con.close()

    # Проверка наличия данных по указанному условию и вывод таблицы, если данные не пусты
    if (data):
        print('')
        # Получение имен полей таблицы
        fields = fieldNames(dbName)
        showFields(fields)
        showData(data)
    else:
        print('В таблице нет строк, удовлетворяющих заданному условию.')
        print('Попробуйте еще раз.')


def updateValues(dbName, cond):
    """Замена значений подмножества
Входные аргументы: имя БД; условие для отбора подмножества строк таблицы
В результате работы функции в таблице указанной БД обновится значение определенного поля всех строк, удовлетворяющих заданному условию"""
    
    # Проверка наличия условия
    if (cond == ''):
        print('Условие отсутствует! Введите условие и повторите попытку.')
        return

    while True:
        new_val = input('Введите имя поля и новое значение (<имя поля> = <новое значение>): ')

        # Проверка имени поля из условия
        if checkField(dbName, new_val):
            break
        
        else:
            print('Несуществующее поле БД! Попробуйте еще раз.')


    # Открытие БД
    con = sqlite3.connect(dbName)
    cur = con.cursor()


    # Создание SQL-запроса
    sql = 'UPDATE {0} SET {1} WHERE {2}'.format(tblname, new_val, cond)
    cur.execute(sql)

    # Получение даты обновления записи
    dat = time.localtime()
    date_of_update = '{:0>2}-{:0>2}-{:0>4}'.format(str(dat.tm_mday), str(dat.tm_mon), str(dat.tm_year))

    print('Дата ', date_of_update)

    # Создание SQL-запроса
    sql = 'UPDATE {0} SET date_of_update="{1}" WHERE {2}'.format(tblname, date_of_update, cond)
    cur.execute(sql)

    # Сохранение изменений
    con.commit()

    # Сохранение изменений
    cur.close()
    con.close()

    print('Значения подмножества изменены')

    tableDisplay(dbName)
    

def delRows(dbName, cond):
    """Удаление подмножества строк из БД
Входные аргументы: имя БД; условие для отбора подмножества строк таблицы
В результате работы функции из таблицы указанной БД будут удалены строки, удовлетворяющие заданному условию"""
    
    # Проверка наличия условия
    if (cond == ''):
        print('Условие отсутствует! Введите условие и повторите попытку.')
        return

    # Открытие БД
    con = sqlite3.connect(dbName)
    cur = con.cursor()

    # Создание SQL-запроса
    sql = 'DELETE FROM {0} WHERE {1}'.format(tblname, cond)

    cur.execute(sql)

    # Сохранение изменений
    con.commit()

    # Закрытие БД
    cur.close()
    con.close()

    print('Подмножество удалено')

    tableDisplay(dbName)
    
#****************************************

print('Здравствуйте! Данная программа позволяет работать с БД, включающей одну таблицу (stud) со следующими полями:')
print('Код дисциплины по учебному предмету - code;')
print('Название дисциплины - subject;')
print('Номер семестра с аттестацией по дисциплине - sem_number;')
print('Тип аттестации (экзамен/зачет) - type_of_cert;')
print('Дата аттестации - date_of_cert;')
print('ФИО преподавателя, проводившего аттестацию - prof_fio;')
print('Должность преподавателя - prof_pos;')
print('Полученная оценка - mark;')
print('Дата занесения/обновления записи - date_of_update.')
print('')

while True:
    dbcrt = input('Хотите создать новую БД? (Y - да; N - нет): ')
    
    # Удаление пробелов в начале и конце строки
    dbcrt = fullSpaceDel(dbcrt)
    
    if (dbcrt.upper() == 'Y' or dbcrt.upper() == 'N'):
        break
    
    elif (dbcrt == 'exit'):
        print('Благодарим за использование данной программы. До свидания!')
        sys.exit()
    
    else:
        print('Неверный ответ! Попробуйте еще раз.')
        print('Для завершения работы программы введите "exit".')

if (dbcrt.upper() == 'Y'):
    my_dbName = input('Введите имя новой БД: ')
    
    # Удаление пробелов в начале и конце строки
    my_dbName = fullSpaceDel(my_dbName)
    
    dbCreate(my_dbName)
    print('БД "{}" создана.'.format(my_dbName))

else:
    while True:
        my_dbName = input('Введите имя существующей БД: ')
        
        # Удаление пробелов в начале и конце строки
        my_dbName = fullSpaceDel(my_dbName)
        
        if (os.path.isfile(my_dbName)):
            break

        elif (my_dbName == 'exit'):
            print('Благодарим за использование данной программы. До свидания!')
            sys.exit()
    
        else:
            print('Неверный файл! Попробуйте еще раз')
            print('Для завершения работы программы введите "exit".')
    

# Словарь с элементами меню
menu_dict = {
    1:'tableDisplay(my_dbName)',
    2:'tableFile(my_dbName)',
    3:'addRow(my_dbName)',
    }

# Условие отбора подмножества
cond = ''

# Словарь с элементами меню второго уровня
subMenu_dict = {
    1:'cond = condEnter(my_dbName)',
    2:'showSubTable(my_dbName, cond)',
    3:'updateValues(my_dbName, cond)',
    4:'delRows(my_dbName, cond)'
    }

# Бесконечный цикл для работы программы (выход из цикла происходит при вводе 0 в меню)
while True:
    choice = menu()
    if (choice == '0'):
        break

    elif (choice > '0' and choice < '4'):
        exec(menu_dict[int(choice)])

    elif (choice == '4'):
        sub_choice = subMenu()
        if (sub_choice == '0'):
            continue

        if (sub_choice < '0' or sub_choice > '4'):
            print('Такого варианта нет! Возврат в главное меню! Попробуйте еще раз.')
            continue
        
        exec(subMenu_dict[int(sub_choice)])
        
    else:
        print('Такого варианта нет! Попробуйте еще раз.')

print('Благодарим за использование данной программы. До свидания!')
