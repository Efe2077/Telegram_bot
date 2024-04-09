import telebot
from telebot import types
from random import choice
from add_new import add_user, add_admin, delete_your_admins


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
new_admin_name = str()
USER_NAME = None


@bot.message_handler(commands=['start', 'hello', 'привет', 'hi'])
def start(message):
    global ADMIN_STATUS, USER_NAME
    bot.send_message(message.chat.id, choice(GREETINGS))
    name = message.from_user.first_name
    bot.send_message(message.chat.id, name)

    USER_NAME = message.chat.username


@bot.message_handler(commands=['bye', 'end', 'пока'])
def bye(message):
    bot.send_message(message.chat.id, choice(GOODBYES))


@bot.message_handler(commands=['command'])
def admin(message):
    NAME, ID = message.from_user.username, message.chat.id
    ADMIN_STATUS = add_user(NAME, ID)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Заказать напиток', callback_data='buy_drink')
    btn2 = types.InlineKeyboardButton('Расписание', callback_data='schedule')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Музыка', callback_data='music')
    btn4 = types.InlineKeyboardButton('Оценки выступления', callback_data='grade')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('Время выступления', callback_data='performance_time')
    btn6 = types.InlineKeyboardButton('Обратиться к организаторам', callback_data='contact_the_organizers')
    markup.row(btn5, btn6)
    btn7 = types.InlineKeyboardButton('FAQ ⁉️', callback_data='F_A_Q')
    btn8 = types.InlineKeyboardButton('Наши соцсети', callback_data='our_social_networks')
    markup.row(btn7, btn8)

    if ADMIN_STATUS:
        btn_for_admin1 = types.InlineKeyboardButton('Добавить админа', callback_data='add_new_admin')
        markup.row(btn_for_admin1)
        btn_for_admin2 = types.InlineKeyboardButton('Удалить админа', callback_data='delete_admin')
        markup.row(btn_for_admin2)

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
        del_admin(callback.message)
    elif callback.data == 'our_social_networks':
        text = open('data/social_networks.txt', 'r', encoding='utf-8').read()
        bot.send_message(callback.message.chat.id, text)


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
        bot.delete_message(message.chat.id, message.message_id - 7)
        bot.delete_message(message.chat.id, message.message_id - 6)
        bot.delete_message(message.chat.id, message.message_id - 5)
        bot.delete_message(message.chat.id, message.message_id - 4)
        bot.delete_message(message.chat.id, message.message_id - 3)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)


def inp_name(message):
    if message.text:
        global new_admin_name, command
        new_admin_name = message.text
        bot.send_message(message.chat.id, f'Такое имя: {new_admin_name}?')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton('✅ Да')
        btn2 = types.KeyboardButton('❌ Нет')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup)


def del_admin(message):
    global command
    command = 'delete_admin'
    bot.send_message(message.chat.id, 'Внимание! Вы можете удалить только тех админов, которых вы добавляли')
    bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' админа")
    bot.register_next_step_handler(message, inp_name)


if __name__ == '__main__':
    bot.polling(none_stop=True)
