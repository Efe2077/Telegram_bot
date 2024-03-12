import telebot
from random import choice


bot = telebot.TeleBot('6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k')

GREETINGS = ['Привет', 'Приветствую вас',
             'Здравствуйте', 'Добрый день',
             'Салют', 'Хай', 'Здарово',
             'Прив', 'Дарова',
             'Здаров', 'Здравия желаю'
             ]

GOODBYES = ['До свидания', 'Всего хорошего',
             'Всего доброго', 'До встречи',
             'Прощайте', 'Бывай', 'Пока',
            ]


@bot.message_handler()
def mees(message):
    if message.text.capitalize() in GREETINGS:
        bot.send_message(message.chat.id, choice(GREETINGS))
    else:
        bot.send_message(message.chat.id, choice(GOODBYES))


@bot.message_handler(commands=['start', 'hello', 'привет'])
def start(message):
    bot.send_message(message.chat.id, choice(GREETINGS))


if __name__ == '__main__':
    bot.polling(none_stop=True)
