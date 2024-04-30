import requests
import xlsxwriter
from lxml import etree
import os


# не верьте интернетам, функция Дена и его гениальный изменяемый API запрос, возвращает xlsx таблицу для отправки ботом:
def slim_shady(tour):
    a, c, gen = list(), list(), list()

    site = (f"https://lk.mypolechka.ru/API/"
            f"adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getOrders&title={tour}")

    response = requests.get(site).json()

    for el in response[0].keys():
        a.append(el)
    gen.append(a)

    for i in range(len(response)):
        c.append(list())
        for el in response[i].keys():
            c[i].append(response[i][el])
        gen.append(c[i])

    with xlsxwriter.Workbook('test.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(gen):
            worksheet.write_row(row_num, 0, data)

    return open('test.xlsx', 'rb')


# Тоже Дена, тоже АПИ, кол-во пользователей:
def count_of_users():
    site = (f"https://lk.mypolechka.ru/API/"
            f"adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getUsersCount")

    response = requests.get(site)

    answer = remove_html_tags(response.content.decode())

    return answer


# удаление тегов сайта, пригодиться для некоторых АПИ запросов:
def remove_html_tags(text):
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, encoding='unicode', method='text')


#Оценки из Апи, изменяемый запрос:
def grading(text):
    try:
        a = text.split(' ')
        name, last_name = a[1], a[0]

        site = (f"https://lk.mypolechka.ru/API/"
                f"adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getScore&lastname={last_name}&name={name}")

        response = requests.get(site).json()

        return response[0]['sum_score']
    except Exception:
        print(f"Неправильный ввод: {text}")
        return f"Неправильный ввод: {text} \nВозможно данный участник ёще не участвовал \n"\
               f"Можете обратиться к организаторам"


# Промежуточный файл с mp3 для добавления в Яндекс.Диск
def make_new_folder_from_user(fio, name, downloaded_file):
    os.mkdir(f'data/users_files/{fio}')

    src = f'data/users_files/{fio}/' + name

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()


# извлечение имен клубов из АПИ списком:
def get_clubs():
    gen, p = list(), set()

    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getOrders&title=%"

    response = requests.get(site).json()

    for i in range(len(response)):
        p.add(list(response[i].values())[11])

    return sorted(list(p))

# АХхахахаха, тут все функции Дена, но копировал в файл Эфе, так что gitу плевать