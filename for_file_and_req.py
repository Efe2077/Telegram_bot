import requests
import xlsxwriter
from lxml import etree
import os


# не верьте интернетам, функция Дена и его гениальный изменяемый API запрос, возвращает xlsx таблицу для отправки ботом:
def slim_shady(tour):
    try:
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
    except Exception:
        print('Slim Shady сбоит')


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


# Оценки индивидуальные из Апи с разделение по видам через обращение к спец. атрибутам, изменяемый запрос:
def ind_grading(text):
    try:
        a = text.split(' ')
        name, last_name = a[1], a[0]

        site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getScore&lastname={last_name}&name={name}"

        response = requests.get(site).json()
        sum_score = response[0]['sum_score']
        ind_text = ''
        ind_text += f'{last_name} {name} - оценки:\n\n'
        in_var_n = 0
        if response[0]['item'] == '0':
            in_var_n = 1
            score = response[0]['score']
            ind_text += f'БП: {score}\n'
        for i in range(in_var_n, len(response)):
            score = response[i]['score']
            if in_var_n == 1:
                ind_text += f'{i} вид: {score}\n'
            else:
                ind_text += f'{i + 1} вид: {score}\n'
        ind_text += f'\nСуммарная оценка: {sum_score}'
        return ind_text
    except Exception:
        print(f"Неправильный ввод: {text}")
        return f"Неправильный ввод: {text} \nВозможно данный участник ёще не участвовал \n"\
               f"Можете обратиться к организаторам"


# Оценки групповые из Апи с разделение по видам через обращение к спец. атрибутам, изменяемый запрос:
def group_grading(text):
    try:
        group_name = text

        site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getScore&lastname={group_name}"

        response = requests.get(site).json()

        sum_score = response[0]['sum_score']
        group_text = ''
        group_text += f'{group_name} - оценки:\n\n'
        g_var_n = 0
        if response[0]['item'] == '0':
            g_var_n = 1
            score = response[0]['score']
            group_text += f'БП: {score}\n'
        for i in range(g_var_n, len(response)):
            score = response[i]['score']
            if g_var_n == 1:
                group_text += f'{i} вид: {score}\n'
            else:
                group_text += f'{i + 1} вид: {score}\n'
        group_text += f'\nСуммарная оценка: {sum_score}'
        print(f"Успешный ввод: {group_name}")
        return group_text
    except Exception:
        print(f"Неправильный ввод: {group_name}")
        return f"Неправильный ввод: {group_name}"


# Промежуточный файл с mp3 для добавления в Яндекс.Диск
def make_new_folder_from_user(fio, name, downloaded_file):
    try:
        os.mkdir(f'data/users_files/{fio}')

        src = f'data/users_files/{fio}/' + name

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()
    except Exception:
        print('make_new_folder_from_user сбоит')


# извлечение имен клубов из АПИ списком:
def get_clubs():
    gen, p = list(), set()

    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getOrders&title=%"

    response = requests.get(site).json()

    for i in range(len(response)):
        p.add(list(response[i].values())[11])

    return sorted(list(p))

# АХхахахаха, тут все функции Дена, но копировал в файл Эфе, так что gitу плевать