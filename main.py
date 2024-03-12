import telebot
from random import choice


bot = telebot.TeleBot('6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k')

GREETINGS = ['Привет!', 'Приветствую вас!',
             'Здравствуйте!', 'Добрый день!',
             'Салют!', 'Хай!', 'Здорово!',
             ]


@bot.message_handler()
def mees(message):
    bot.send_message(message.chat.id, choice(GREETINGS))


@bot.message_handler(commands=['start', 'hello', 'привет'])
def start(message):
    bot.send_message(message.chat.id, choice(GREETINGS))


if __name__ == '__main__':
    bot.polling(none_stop=True)
