import sqlite3


def send_questions(user_id, question):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Questions FROM Users WHERE Id = ?""", (user_id, )).fetchall()

    if question not in result[0][0].split('#'):
        if result[0][0] == 'No_questions':  # Если это первый вопрос
            cur.execute(f"""UPDATE Users SET Questions = '{question}#&{user_id}' WHERE Id = '{user_id}' """)

        else:   # Если это НЕ первый вопрос
            question = f'{question}#{result[0][0]}'
            cur.execute(f"""UPDATE Users SET Questions = '{question}' WHERE Id = '{user_id}' """)
    else:
        print('Вы уже задавали такой вопрос')

    con.commit()
    con.close()


def delete_questions(user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET Questions = 'No_questions' WHERE Id = '{user_id}'""").fetchall()

    con.commit()
    con.close()


def show_questions():
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Questions FROM Users WHERE Questions != 'No_questions' """).fetchall()
    list_of_questions = []

    for num, el in enumerate(result):
        list_of_questions.append((num + 1, el[0].split('#')))

    con.commit()
    con.close()

    return list_of_questions


delete_questions(1025291843)