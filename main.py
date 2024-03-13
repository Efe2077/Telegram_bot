import telebot
from random import choice
from add_new_user import add_user


bot = telebot.TeleBot('6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k')

GREETINGS = ['Привет', 'Приветствую вас',
             'Здравствуйте', 'Добрый день',
             'Салют', 'Хай', 'Здравия желаю'
             ]

GOODBYES = ['До свидания', 'Всего хорошего',
             'Всего доброго', 'До встречи',
             'Прощайте', 'Бывай', 'Пока',
            ]


@bot.message_handler(commands=['start', 'hello', 'привет'])
def start(message):
    bot.send_message(message.chat.id, choice(GREETINGS))
    NAME, ID = message.from_user.username, message.chat.id
    text = f"Статус Админа: {add_user(NAME, ID)}"
    bot.send_message(message.chat.id, text)


@bot.message_handler()
def mees(message):
    bot.send_message(message.chat.id, message.json['text'])


if __name__ == '__main__':
    bot.polling(none_stop=True)
