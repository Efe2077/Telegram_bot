import telebot
from telebot import types
from random import choice
from add_new import add_user, add_admin, delete_your_admins


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
new_admin_name = str()
USER_NAME = None


@bot.message_handler(commands=['start', 'hello', 'привет'])
def start(message):
    global ADMIN_STATUS, USER_NAME
    bot.send_message(message.chat.id, choice(GREETINGS))
    name = message.from_user.first_name
    bot.send_message(message.chat.id, name)

    USER_NAME = message.chat.username


@bot.message_handler(commands=['bye', 'end', 'пока'])
def bye(message):
    bot.send_message(message.chat.id, choice(GOODBYES))


@bot.message_handler(commands=['admin'])
def admin(message):
    NAME, ID = message.from_user.username, message.chat.id
    ADMIN_STATUS = add_user(NAME, ID)
    if ADMIN_STATUS:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Добавить админа', callback_data='add_new_admin')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Удалить админа', callback_data='delete_admin')
        markup.row(btn2)
        bot.send_message(message.chat.id, 'Вы можете выполнить такие функции:', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Вы не являетесь админом')


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
    elif callback.data == 'answer_yes':
        if command == 'add_admin':
            bot.send_message(callback.message.chat.id, new_admin_name)
            add_admin(USER_NAME, new_admin_name)

        elif command == 'delete_admin':
            delete_your_admins(USER_NAME, new_admin_name)

    elif callback.data == 'answer_no':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Написать имя еще раз', callback_data='add_new_admin')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Назад', callback_data='return')
        markup.row(btn2)
        bot.send_message(callback.message.chat.id, 'Выберете:', reply_markup=markup)

    elif callback.data == 'return':
        callback.data = None

        bot.delete_message(callback.message.chat.id, callback.message.message_id - 5)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 4)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 3)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)


def inp_name(message):
    if message.text and message.text != 'return':
        global new_admin_name, command
        new_admin_name = message.text
        bot.send_message(message.chat.id, f'Такое имя: {new_admin_name}?')

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Да', callback_data='answer_yes')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Нет', callback_data='answer_no')
        markup.row(btn2)
        bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup)


def del_admin(message):
    global command
    command = 'delete_admin'
    bot.send_message(message.chat.id, 'Внимание! Вы можете удалить только тех админов, которых вы добавляли')
    bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' админа")
    bot.register_next_step_handler(message, inp_name)


@bot.message_handler()
def mees(message):
    bot.send_message(message.chat.id, message.json['text'])


if __name__ == '__main__':
    bot.polling(none_stop=True)
