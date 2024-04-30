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
        list_of_text.append(el[0])

    result = cur.execute(f"""SELECT photo, text FROM Users WHERE photo != 'None' """).fetchall()
    e = {}
    q = 0
    for i in result:
        q += 1
        w = 'пост №' + str(q)
        e[w] = [i[0], i[1]]
    return e


def delete_suggestions(photo, text):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET Photo = 'None' WHERE Photo = '{photo}'""").fetchall()
    cur.execute(f"""UPDATE Users SET text = 'None' WHERE text = '{text}'""").fetchall()
    con.commit()
    con.close()


def get_id_from_suggestion(text):
    if text != 'None':
        con = sqlite3.connect('Users.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT Id FROM Users WHERE photo == '{text}' """).fetchall()

        con.commit()
        con.close()

        print(result)

        if result:
            return result[0][0]
        else:
            return 'На данный вопрос уже ответили'