import sqlite3


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
        w = 'Пост №' + str(q)
        print(i[1], w)
        cur.execute(f"""UPDATE Users SET Printed_sug_2 = '{w}' WHERE Photo = '{i[0]}' """).fetchall()
        e[w] = [i[0], i[1]]
    return e


def delete_suggestions(num):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET Photo = null WHERE Printed_sug_2 = '{num}' """).fetchall()
    cur.execute(f"""UPDATE Users SET Text = null WHERE Printed_sug_2 = '{num}' """).fetchall()
    cur.execute(f"""UPDATE Users SET Printed_sug_2 = null WHERE Printed_sug_2 = '{num}' """).fetchall()

    con.commit()
    con.close()


def get_id_from_suggestion(text):
    if text != 'None':
        con = sqlite3.connect('Users.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT Id FROM Users WHERE text == '{text}' """).fetchall()

        con.commit()
        con.close()

        if result:
            return result[0][0]
        else:
            return 'На данный вопрос уже ответили'


show_suggestion()