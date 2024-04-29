import telebot
import sqlite3

# Создание бота
bot = telebot.TeleBot("YOUR_BOT_TOKEN")


# Получение всех админов
admins = ['ADMIN_ID_1', 'ADMIN_ID_2']  # Заменить ADMIN_ID_1, ADMIN_ID_2 на id админов

# Обработка команды для отправки поста
def post(message):
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()

    user_id = message.chat.id
    text = message.text.split(' ', 1)[1]
    bot.send_message(admins[0], f"Новый пост от пользователя {user_id}: {text}")
    cursor.execute('INSERT INTO posts (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()

# Обработка команды для добавления фото к посту

def send_suggestion(user_id, question):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT photo FROM Users WHERE Id = ?""", (user_id, )).fetchall()
    cur.execute(f"""UPDATE Users SET photo = '{question}' WHERE Id = '{user_id}' """)

    con.commit()
    con.close()

# Обработка команды для ответа на пост


def send_suggestion_text(user_id, question):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT text FROM Users WHERE Id = ?""", (user_id, )).fetchall()
    cur.execute(f"""UPDATE Users SET text = '{question}' WHERE Id = '{user_id}' """)

    con.commit()
    con.close()
def show_suggestion():
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT text FROM Users WHERE photo != 'None' """).fetchall()
    list_of_text = []

    for num, el in enumerate(result):
        list_of_text.append((num + 1, el[0]))

    result = cur.execute(f"""SELECT photo FROM Users WHERE photo != 'None' """).fetchall()
    list_of_photo = []

    for num, el in enumerate(result):
        list_of_photo.append((num + 1, el[0]))
    con.commit()
    con.close()

    return list_of_text, list_of_photo