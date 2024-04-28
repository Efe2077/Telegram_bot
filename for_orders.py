import sqlite3


def send_orders(user_id, question):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Questions FROM Users WHERE Id = ?""", (user_id, )).fetchall()

    if question not in result[0][0].split():
        if result[0][0] == 'No_orders':  # Если это первый заказ
            cur.execute(f"""UPDATE Users SET Orders = '{question}' WHERE Id = '{user_id}' """)
        else:   # Если это НЕ первый вопрос
            question = f'{result[0][0]} {question}'
            cur.execute(f"""UPDATE Users SET Orders = '{question}' WHERE Id = '{user_id}' """)
    else:
        print('Вы уже задавали такой вопрос')

    con.commit()
    con.close()


def delete_orders(text):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET Orders = 'No_orders' WHERE Orders = '{text}'""").fetchall()

    con.commit()
    con.close()


def show_orders():
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Orders FROM Users WHERE Orders != 'No_orders' """).fetchall()
    list_of_questions = []

    for num, el in enumerate(result):
        list_of_questions.append((num + 1, el[0]))

    con.commit()
    con.close()

    return list_of_questions


def get_id_from_order(text):
    if text != 'No_orders':
        con = sqlite3.connect('Users.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT Id FROM Users WHERE Orders == '{text}' """).fetchall()

        con.commit()
        con.close()

        print(result)

        if result:
            return result[0][0]
        else:
            return 'Данный заказ уже собрали'