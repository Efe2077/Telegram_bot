from lxml import etree

import telebot
import requests
import xlsxwriter
from telebot import types
from random import choice
from telebot.types import ReplyKeyboardRemove
from for_questions import send_questions, show_questions, get_id_from_question, delete_questions
from add_new import add_user, add_admin, delete_your_admins

# 7050246509:AAHKETNv4k6_Z6FQ37bkCh1QJlqFABpJ2Mo - основной
# 6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k - мой
bot = telebot.TeleBot('6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k')


GREETINGS = ['Привет', 'Приветствую вас',
             'Здравствуйте', 'Добрый день',
             'Салют', 'Хай', 'Здравия желаю'
             ]

GOODBYES = ['До свидания', 'Всего хорошего',
            'Всего доброго', 'До встречи',
            'Прощайте', 'Бывай', 'Пока',
            ]

command = None
ADMIN_STATUS = None
new_text = None
USER_NAME = None
quest = None
printed_work = [None, None]
consult = show_questions()


# def start_markup():
#     markup = types.InlineKeyboardMarkup(row_width=True)
#     link_keyboard1 = types.InlineKeyboardButton(text="канал", url="https://t.me/gymnastkapolechka")
#     link_keyboard2 = types.InlineKeyboardButton(text="2 канал", url="https://t.me/rg_child_league")
#     check_keyboard = types.InlineKeyboardButton(text="Проверить", callback_data="check")
#     markup.add(link_keyboard1, link_keyboard2, check_keyboard)
#
#     return markup


@bot.message_handler(commands=['start', 'hello', 'привет', 'hi'])
def start(message):
    global ADMIN_STATUS, USER_NAME
    bot.send_message(message.chat.id, choice(GREETINGS))
    name = message.from_user.first_name

    if name == 'Uniade bot':
        name = message.chat.first_name
        USER_NAME = message.chat.username

    bot.send_message(message.chat.id, name)

    # if check(message, message.chat.id) and check_channels_start(message):
    if True:
        admin(message)


# def check(message, chat_id):
#     st = bot.get_chat_member(chat_id, user_id=message.chat.id).status
#     return st in ["creator", "administrator", "member"]


# def check_channels_start(message):
#     markup = types.InlineKeyboardMarkup(row_width=True)
#     if check(message, "-1001649523664") and check(message, '-1001729713697'):
#         bot.send_message(message.chat.id, "Спасибо за подписку ✨")
#         markup.add(admin(message))
#     else:
#         bot.send_message(message.chat.id, "Подпишись на каналы", reply_markup=start_markup())
#
#
# def check_channels(message):
#     if check(message, "-1001649523664") and check(message, '-1001729713697'):
#         return True
#     else:
#         bot.send_message(message.chat.id, "Подпишись на каналы", reply_markup=start_markup())


def admin(message):
    a = bot.send_message(message.chat.id, 'delete', reply_markup=ReplyKeyboardRemove())
    bot.delete_message(message.chat.id, a.message_id)

    markup = make_main_markup(message)

    bot.send_message(message.chat.id, 'Вы можете выполнить такие функции:', reply_markup=markup)


@bot.message_handler(commands=['bye', 'end', 'пока'])
def bye(message):
    bot.send_message(message.chat.id, choice(GOODBYES))


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # if check(callback.message, callback.message.chat.id) and check_channels(callback.message):
    if True:
        global command, USER_NAME
        USER_NAME = callback.message.chat.username
        print(command)
        if callback.data == 'add_new_admin':
            bot.send_message(callback.message.chat.id, "Напишите 'Имя пользователя в телеграмме' вашего нового админа")

            file = open('data/telegram_username.jpg', 'rb')
            bot.send_photo(callback.message.chat.id, file)
            command = 'add_admin'
            bot.register_next_step_handler(callback.message, inp_name)
        elif callback.data == 'delete_admin':
            command = 'delete_admin'
            del_admin(callback.message)
        elif callback.data == 'our_social_networks':
            text = open('data/social_networks.txt', 'r', encoding='utf-8').read()
            bot.send_message(callback.message.chat.id, text)
        elif callback.data == 'music':
            bot.send_message(callback.message.chat.id, 'https://music.yandex.ru/album/22747037/track/105213792')
            admin(callback.message)
        elif callback.data == 'buy_drink':
            bot.send_message(callback.message.chat.id, "Сделайте заказ")
            command = 'drink'
            bot.register_next_step_handler(callback.message, inp_question)
        # elif callback.data == 'check':
        #     start(callback.message)
        elif callback.data == 'F_A_Q':
            bot.edit_message_text(f'Вопросы:',
                                  reply_markup=questions(),
                                  chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id)
        elif callback.data == 'grade':
            bot.send_message(callback.message.chat.id, "Введите Фамилию Имя гимнастки:")
            bot.register_next_step_handler(callback.message, grade)
        elif callback.data == 'show_questions_from_users':
            show_questions_from_users(callback.message)
        elif callback.data == 'send_questions':
            bot.send_message(callback.message.chat.id, "Напишите вопрос")
            bot.register_next_step_handler(callback.message, inp_question)
            # ask(callback.message)
            # send_questions(callback.message.chat.id, quest)
            # admin(callback.message)

        elif callback.data in ['Московская зима 2024', 'Спортивная Весна 2024', 'Зимняя Сказка 2023', 'Маленькая принцесса 2024']:
            slim_shady(callback.message, callback.data)

        elif callback.data.isdigit():
            if [i for i in consult if int(callback.data) == i[0]] and callback.data.isdigit():
                global printed_work
                command = 'answer_to_question'
                bot.send_message(callback.message.chat.id, f"Вы выбрали '{consult[int(callback.data) - 1][1]}'")
                printed_work[0] = consult[int(callback.data) - 1][1]
                bot.register_next_step_handler(callback.message, answer)

        # Временная кнопка
        elif callback.data == 'show_count_of_users':
            count_of_users(callback.message)
        elif callback.data == 'table':
            table(callback.message)
        elif callback.data == 'text_live':
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Трансляция', url='https://vk.com/textlive547685'))
            bot.reply_to(callback.message,
                         'Скорее смотреть!!!',
                         reply_markup=markup)
        elif callback.data == 'video_live':
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Трансляция', url='https://vk.com/video-211067501_456239145'))
            bot.reply_to(callback.message,
                         'Скорее смотреть!!!',
                         reply_markup=markup)
        elif callback.data == 'qw_1':
            # file = open('data/checkroom0.jpg', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id,
                             'Войдя через главный вход, проходите через турникет и заворачиваете направо')
            # file = open('data/checkroom1.jpg', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id, 'проходите по коридору вперед')
            # file = open('data/checkroom2.jpg', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id, 'поворачиваете налево и входите в раздевалку, вы на месте!')
            # ret(callback)
        elif callback.data == 'qw_2':
            # file = open('data/rating1.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
            bot.reply_to(callback.message,
                         'Зарегистрироваться на сайте (если еще этого не сделали), в профиле выбрать "достижения"',
                         reply_markup=markup)
            # file = open('data/rating2.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id,
                             'В разделе достижения будет указано значения рейтинга (твой рейтинг) и достижения')
            # ret(callback)
        elif callback.data == 'qw_3':
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Помочь!', url='https://t.me/rg_child_league/491'))
            bot.reply_to(callback.message,
                         'Для начала нужно набрать 100 реакций XD',
                         reply_markup=markup)
            # ret(callback)
        elif callback.data == 'qw_4':
            bot.send_message(callback.message.chat.id, 'Фото будут доступны на сайте ниже с 16 апреля')
            # file = open('data/photo_qr.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Заказать', url='http://kondakov.online/order.html'))
            bot.reply_to(callback.message,
                         'Сайт с фотографиями',
                         reply_markup=markup)
            # ret(callback)
        elif callback.data == 'qw_5':
            bot.send_message(callback.message.chat.id, 'ответ 5')
            # ret(callback)
        elif callback.data == 'qw_6':
            bot.send_message(callback.message.chat.id,
                             'Чтобы судьи понимали тайминг упражнения, соответствующий правилам!')
            # ret(callback)
        elif callback.data == 'qw_7':
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    'Скорее смотреть!!!', url='https://vk.com/textlive547685'))
            bot.reply_to(callback.message,
                         'Подайте заявку на вступление в сообщество. '
                         'Когда она будет принята, Вы сможете узнать в репортаже',
                         reply_markup=markup)
            # ret(callback)
        elif callback.data == 'qw_8':
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    'Скорее смотреть!!!', url='https://vk.com/textlive547685'))
            bot.reply_to(callback.message,
                         'Подайте заявку на вступление в сообщество. '
                         'Когда она будет принята, Вы сможете увидеть долгожданные выступления',
                         reply_markup=markup)
            # ret(callback)
        elif callback.data == 'qw_9':
            # file = open('data/online1.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
            bot.reply_to(callback.message,
                         'Зарегистрироваться на сайте (если еще этого не сделали), в профиле выбрать "подать заявку"',
                         reply_markup=markup)
            # file = open('data/online2.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id,
                             'При оплате выбрать "онлайн"')
            # ret(callback)
        elif callback.data == 'qw_11':
            bot.send_message(callback.message.chat.id, 'Справа от входа в арку находится стол dj, '
                                                       'именно этому харизматичному мужчине нужно сдать флешку XD')
            # file = open('data/dj.jpg', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            # ret(callback)
        elif callback.data == 'qw_10':
            # file = open('data/photo1.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
            bot.reply_to(callback.message,
                         'Зарегистрироваться на сайте (если еще этого не сделали), '
                         'в профиле выбрать "загрузить фото для турнира"',
                         reply_markup=markup)
            # file = open('data/photo2.png', 'rb')
            # bot.send_photo(callback.message.chat.id, file)
            bot.send_message(callback.message.chat.id,
                             'Далее нажмите "Загрузить фото"')
            # ret(callback)
        # elif callback.data == 'qw_12':
        #     bot.send_message(callback.message.chat.id, 'ответ 10')
        #     ret(callback)
        elif callback.data == 'qw_quit':
            bot.edit_message_text(f'Вы можете выполнить такие функции:',
                                  reply_markup=make_main_markup(callback.message),
                                  chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id)


@bot.message_handler(content_types=['text'])
def func(message):
    global command
    print(command)
    if message.text == "✅ Да":
        if command == 'add_admin':
            mess = add_admin(USER_NAME, new_text)
            bot.send_message(message.chat.id, mess)
            admin(message)

        elif command == 'delete_admin':
            mess = delete_your_admins(USER_NAME, new_text)
            bot.send_message(message.chat.id, mess)
            admin(message)

    elif message.text == "❌ Нет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton('Написать еще раз')
        btn2 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Выберете:', reply_markup=markup)

    elif message.text == 'Написать еще раз':
        bot.send_message(message.chat.id, "Повторите")
        bot.register_next_step_handler(message, inp_name)

    elif message.text == 'Назад':
        admin(message)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти в вк', url='https://vk.com/rg_child_league'))
    bot.reply_to(message, 'Здорово! Не хотите ли Вы предложить это фото для поста в канале?', reply_markup=markup)


# Тут
def inp_name(message):
    global new_text, command
    new_text = message.text
    bot.send_message(message.chat.id, f'Такое имя: {new_text}?')
    yes_or_no(message)


def yes_or_no(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    btn1 = types.KeyboardButton('✅ Да')
    btn2 = types.KeyboardButton('❌ Нет')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup)


def buy_drink(message):
    bot.send_message(message.chat.id, f'Ваш напиток - {message.text}')
    admin(message)


def count_of_users(message):
    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getUsersCount"

    response = requests.get(site)

    bot.send_message(message.chat.id, remove_html_tags(response.content.decode()))
    admin(message)


def remove_html_tags(text):
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, encoding='unicode', method='text')


def map(message):
    text = message.text
    bot.send_message(message.chat.id, f'Такое место: {text}?')
    API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
    site = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={text}&format=json"

    response = requests.get(site)

    position = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    answer = f'll={",".join(position.split())}'

    resp = requests.get(f"http://static-maps.yandex.ru/1.x/?{answer}&z=16&l=map")
    map_file = "data/map.jpg"
    with open(map_file, "wb") as file:
        file.write(resp.content)

    file = open('data/map.jpg', 'rb')
    bot.send_photo(message.chat.id, file)
    admin(message)


def questions():
    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton('Где раздевалка?', callback_data='qw_1')) #фото-ряд
    markup2.add(types.InlineKeyboardButton('Где найти рейтинг Юниады?', callback_data='qw_2')) #https://uniade.world/profile
    markup2.add(types.InlineKeyboardButton('Как посмотреть оценки?', callback_data='qw_3')) #нужно набрать 100 реакций https://t.me/rg_child_league/491
    markup2.add(types.InlineKeyboardButton('Как заказать фотографии?', callback_data='qw_4'))
    markup2.add(types.InlineKeyboardButton('Как найти визажиста на турнире?', callback_data='qw_5'))
    markup2.add(types.InlineKeyboardButton('Зачем нужен гонг?', callback_data='qw_6'))
    markup2.add(types.InlineKeyboardButton('Какой поток выступает?', callback_data='qw_7'))
    markup2.add(types.InlineKeyboardButton('Как посмотреть трансляцию?', callback_data='qw_8'))
    markup2.add(types.InlineKeyboardButton('Как поучаствовать в Юниаде онлайн?', callback_data='qw_9'))
    markup2.add(types.InlineKeyboardButton('Как загрузить фото, чтобы попасть на экран?', callback_data='qw_10'))
    markup2.add(types.InlineKeyboardButton('Куда сдавать музыку?', callback_data='qw_11'))
    #markup2.add(types.InlineKeyboardButton('Кто разработал бот?', callback_data='qw_12'))
    #markup2.add(types.InlineKeyboardButton('Как пройти в зал соревнований?', callback_data='qw_13'))
    markup2.add(types.InlineKeyboardButton('выйти', callback_data='qw_quit'))
    return markup2


def del_admin(message):
    bot.send_message(message.chat.id, 'Внимание! Вы можете удалить только тех админов, которых вы добавляли')
    bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' админа")
    bot.register_next_step_handler(message, inp_name)


def inp_question(message):
    global new_text
    new_text = message.text
    ask(message)
    send_questions(message.chat.id, quest)
    admin(message)


def ask(message):
    global quest
    text = new_text
    bot.send_message(message.chat.id, f"Ваш вопрос:\n{text}")
    quest = text


def answer(message):
    global printed_work
    text = message.text
    bot.send_message(message.chat.id, f'Ваш ответ: {text}')
    printed_work[1] = text
    send_answer_from_admin(get_id_from_question(printed_work[0]), printed_work[1])
    admin(message)


def grade(message):
    b = message.text

    try:
        a = message.text.split(' ')
        name, last_name = a[1], a[0]

        site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getScore&lastname={last_name}&name={name}"

        response = requests.get(site).json()

        bot.send_message(message.chat.id, response[0]['sum_score'])
        admin(message)
    except Exception:
        print(f"Неправильный ввод: {b}")
        bot.send_message(message.chat.id, f"Неправильный ввод: {b} \nВозможно данный участник ёще не участвовал \n"
                                          f"Можете обратиться к организаторам")


def show_questions_from_users(message):
    global consult
    markup = types.InlineKeyboardMarkup()
    consult = show_questions()
    for i in consult:
        markup.add(types.InlineKeyboardButton(f'{i[1]}', callback_data=i[0]))
    bot.send_message(message.chat.id, 'Вопросы:', reply_markup=markup)


def send_answer_from_admin(id_of_user, text):
    bot.send_message(id_of_user, f'Ответ от админа: {text}')
    delete_questions(printed_work[0])


def table(message):

    gen, p = list(), set()

    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getOrders&title=%"

    response = requests.get(site).json()

    for i in range(len(response)):
        p.add(list(response[i].values())[11])

    markup = types.InlineKeyboardMarkup()
    consult = p
    for i in consult:
        markup.add(types.InlineKeyboardButton(f'{i}', callback_data=i))
    bot.send_message(message.chat.id, 'Выберите интересующий турнир:', reply_markup=markup)


def slim_shady(message, tour):
    a, c, gen = list(), list(), list()

    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getOrders&title={tour}"

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

    with open('test.xlsx', 'rb') as f1:
        bot.send_document(message.chat.id, f1)
        f1.close()

    admin(message)


def make_main_markup(message):
    global ADMIN_STATUS
    name, id = message.from_user.username, message.chat.id
    if name == 'Uniade_bot':
        name = message.chat.username
    ADMIN_STATUS = add_user(name, id)
    markup = types.InlineKeyboardMarkup()
    #btn1 = types.InlineKeyboardButton('Напитки', callback_data='buy_drink')
    #btn2 = types.InlineKeyboardButton('Предложка', callback_data='suggestion')
    #markup.row(btn1, btn2)
    #btn3 = types.InlineKeyboardButton('Музыка', callback_data='music')
    #markup.row(btn3)
    btn4 = types.InlineKeyboardButton('Оценки выступления', callback_data='grade')
    markup.row(btn4)
    #btn5 = types.InlineKeyboardButton('Время выступления', callback_data='performance_time')
    #markup.row(btn5)
    btn6 = types.InlineKeyboardButton('Обратиться к организаторам', callback_data='send_questions')
    markup.row(btn6)
    btn7 = types.InlineKeyboardButton('ЧаВо⁉️', callback_data='F_A_Q')
    btn8 = types.InlineKeyboardButton('О нас', callback_data='our_social_networks')
    markup.row(btn7, btn8)
    btn9 = types.InlineKeyboardButton('Видео-live', callback_data='video_live')
    btn10 = types.InlineKeyboardButton('Репортаж', callback_data='text_live')
    markup.row(btn9, btn10)
    if ADMIN_STATUS:
        btn_for_admin1 = types.InlineKeyboardButton('Добавить админа', callback_data='add_new_admin')
        markup.row(btn_for_admin1)
        btn_for_admin2 = types.InlineKeyboardButton('Удалить админа', callback_data='delete_admin')
        markup.row(btn_for_admin2)
        btn_for_admin3 = types.InlineKeyboardButton('Вопросы от пользователей', callback_data='show_questions_from_users')
        markup.row(btn_for_admin3)
        # Временная кнопка
        btn_for_admin3 = types.InlineKeyboardButton('Количество пользователей', callback_data='show_count_of_users')
        markup.row(btn_for_admin3)
        # Временная кнопка
        btn_for_admin4 = types.InlineKeyboardButton('Таблица участников', callback_data='table')
        markup.row(btn_for_admin4)

    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True)
