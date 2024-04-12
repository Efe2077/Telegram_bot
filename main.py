import telebot
import requests
from telebot import types
from random import choice
from for_questions import send_questions, show_questions, get_id_from_question, delete_questions
from add_new import add_user, add_admin, delete_your_admins

# 7050246509:AAHKETNv4k6_Z6FQ37bkCh1QJlqFABpJ2Mo - основной
# 6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k - мой
bot = telebot.TeleBot('7050246509:AAHKETNv4k6_Z6FQ37bkCh1QJlqFABpJ2Mo')


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
new_admin_name = None
USER_NAME = None
quest = None
printed_work = [None, None]
consult = show_questions()


@bot.message_handler(commands=['start', 'hello', 'привет', 'hi'])
def start(message):
    global ADMIN_STATUS, USER_NAME
    bot.send_message(message.chat.id, choice(GREETINGS))
    name = message.from_user.first_name
    bot.send_message(message.chat.id, name)
    USER_NAME = message.chat.username

    admin(message)


@bot.message_handler(commands=['bye', 'end', 'пока'])
def bye(message):
    bot.send_message(message.chat.id, choice(GOODBYES))


@bot.message_handler(commands=['command'])
def admin(message):
    global ADMIN_STATUS
    name, id = message.from_user.username, message.chat.id
    if name == 'Uniade_bot' or name == 'Program_by_DED_bot':
        name = message.chat.username
    ADMIN_STATUS = add_user(name, id)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Напитки', callback_data='buy_drink')
    btn2 = types.InlineKeyboardButton('Расписание', callback_data='schedule')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Музыка', callback_data='music')
    markup.row(btn3)
    btn4 = types.InlineKeyboardButton('Оценки выступления', callback_data='grade')
    markup.row(btn4)
    btn5 = types.InlineKeyboardButton('Время выступления', callback_data='performance_time')
    markup.row(btn5)
    btn6 = types.InlineKeyboardButton('Обратиться к организаторам', callback_data='contact_the_organizers')
    markup.row(btn6)
    btn7 = types.InlineKeyboardButton('FAQ ⁉️', callback_data='F_A_Q')
    btn8 = types.InlineKeyboardButton('Наши соцсети', callback_data='our_social_networks')
    markup.row(btn7, btn8)
    # btn9 = types.InlineKeyboardButton('Типа кнопка', callback_data='our_social_networks')
    # markup.row(btn9)

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


    bot.send_message(message.chat.id, 'Вы можете выполнить такие функции:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global command, USER_NAME
    USER_NAME = callback.message.chat.username
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
    elif callback.data == 'buy_drink':
        bot.send_message(callback.message.chat.id, "Сделайте заказ")
        command = 'drink'
        bot.register_next_step_handler(callback.message, buy_drink)
    elif callback.data == 'F_A_Q':
        questions(callback.message)
    elif callback.data == 'grade':
        bot.send_message(callback.message.chat.id, "Напишите место")
        bot.register_next_step_handler(callback.message, map)
    elif callback.data == 'contact_the_organizers':
        bot.send_message(callback.message.chat.id, "Напишите вопрос")
        command = 'send_questions'
        bot.register_next_step_handler(callback.message, ask)
    elif callback.data == 'show_questions_from_users':
        show_questions_from_users(callback.message)

    # Ошибка
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

    elif callback.data == 'qw_1':
        bot.send_message(callback.message.chat.id, 'ответ 1')
        ret(callback)
    elif callback.data == 'qw_2':
        bot.send_message(callback.message.chat.id, 'ответ 2')
        ret(callback)
    elif callback.data == 'qw_3':
        bot.send_message(callback.message.chat.id, 'ответ 3')
        ret(callback)
    elif callback.data == 'qw_4':
        bot.send_message(callback.message.chat.id, 'ответ 4')
        ret(callback)
    elif callback.data == 'qw_5':
        bot.send_message(callback.message.chat.id, 'ответ 5')
        ret(callback)
    elif callback.data == 'qw_6':
        bot.send_message(callback.message.chat.id, 'ответ 6')
        ret(callback)
    elif callback.data == 'qw_7':
        bot.send_message(callback.message.chat.id, 'ответ 7')
        ret(callback)
    elif callback.data == 'qw_8':
        bot.send_message(callback.message.chat.id, 'ответ 8')
        ret(callback)
    elif callback.data == 'qw_9':
        bot.send_message(callback.message.chat.id, 'ответ 9')
        ret(callback)
    elif callback.data == 'qw_10':
        bot.send_message(callback.message.chat.id, 'ответ 10')
        ret(callback)
    elif callback.data == 'qw_quit':
        admin(callback.message)


@bot.message_handler(content_types=['text'])
def func(message):
    global command
    if message.text == "✅ Да":
        if command == 'add_admin':
            mess = add_admin(USER_NAME, new_admin_name)
            bot.send_message(message.chat.id, mess)

        elif command == 'delete_admin':
            mess = delete_your_admins(USER_NAME, new_admin_name)
            bot.send_message(message.chat.id, mess)

        elif command == 'send_questions':
            send_questions(message.chat.id, quest)

        elif command == 'answer_to_question':
            send_answer_from_admin(get_id_from_question(printed_work[0]), printed_work[1])
    elif message.text == "❌ Нет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton('Написать имя еще раз')
        btn2 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Выберете:', reply_markup=markup)
    elif message.text == 'Написать имя еще раз':
        bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' вашего нового админа")

        file = open('data/telegram_username.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
        command = 'add_admin'
        bot.register_next_step_handler(message, inp_name)

    elif message.text == 'Назад':
        for number in range(-7, +1, +1):
            bot.delete_message(message.chat.id, message.message_id + number)

    elif message.text == 'К вопросам':
        questions(message)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти в вк', url='https://vk.com/rg_child_league'))
    bot.reply_to(message, 'Здорово! Не хотите ли Вы предложить это фото для поста в канале?', reply_markup=markup)


def inp_name(message):
    if message.text:
        global new_admin_name, command
        new_admin_name = message.text
        bot.send_message(message.chat.id, f'Такое имя: {new_admin_name}?')
        yes_or_no(message)


def yes_or_no(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('✅ Да')
    btn2 = types.KeyboardButton('❌ Нет')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup)


def buy_drink(message):
    bot.send_message(message.chat.id, f'Ваш напиток - {message.text}')


def ret(callback):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton('К вопросам'))
    bot.send_message(callback.message.chat.id, '.', reply_markup=markup)


# Временная функция
def count_of_users(message):
    site = f"https://lk.mypolechka.ru/API/adminAPI.php?userid=LNnZH53yTPbCv1vrRcGujfqvbZF3&funcid=getUsersCount"

    response = requests.get(site)

    bot.send_message(message.chat.id, response.content.decode())


def map(message):
    text = message.text
    if text:
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


def questions(message):
    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton('вопрос 1', callback_data='qw_1'))
    markup2.add(types.InlineKeyboardButton('вопрос 2', callback_data='qw_2'))
    markup2.add(types.InlineKeyboardButton('вопрос 3', callback_data='qw_3'))
    markup2.add(types.InlineKeyboardButton('вопрос 4', callback_data='qw_4'))
    markup2.add(types.InlineKeyboardButton('вопрос 5', callback_data='qw_5'))
    markup2.add(types.InlineKeyboardButton('вопрос 6', callback_data='qw_6'))
    markup2.add(types.InlineKeyboardButton('вопрос 7', callback_data='qw_7'))
    markup2.add(types.InlineKeyboardButton('вопрос 8', callback_data='qw_8'))
    markup2.add(types.InlineKeyboardButton('вопрос 9', callback_data='qw_9'))
    markup2.add(types.InlineKeyboardButton('вопрос 10', callback_data='qw_10'))
    markup2.add(types.InlineKeyboardButton('выйти', callback_data='qw_quit'))
    bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup2)


def del_admin(message):
    bot.send_message(message.chat.id, 'Внимание! Вы можете удалить только тех админов, которых вы добавляли')
    bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' админа")
    bot.register_next_step_handler(message, inp_name)


def ask(message):
    global quest
    text = message.text
    bot.send_message(message.chat.id, f"Ваш вопрос:\n{text}")
    quest = text
    yes_or_no(message)


def show_questions_from_users(message):
    global consult
    markup = types.InlineKeyboardMarkup()
    consult = show_questions()
    for i in consult:
        markup.add(types.InlineKeyboardButton(f'{i[1]}', callback_data=i[0]))
    bot.send_message(message.chat.id, 'Вопросы:', reply_markup=markup)


def answer(message):
    global printed_work
    text = message.text
    bot.send_message(message.chat.id, text)
    printed_work[1] = text
    yes_or_no(message)


def send_answer_from_admin(id_of_user, text):
    bot.send_message(id_of_user,f'Ответ от админа: {text}')
    delete_questions(printed_work[0])


if __name__ == '__main__':
    bot.polling(none_stop=True)
