import sqlite3


def send_questions(user_id, question):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Questions FROM Users WHERE Id = '{user_id}' """).fetchall()

    if question is not None:
        if result[0][0] is None:  # Если это первый вопрос
            cur.execute(f"""UPDATE Users SET Questions = '{question}' WHERE Id = '{user_id}' """)

        else:
            if question not in result[0][0].split():  # Если это НЕ первый вопрос и он не повторяется
                question = f'{result[0][0]} {question}'
                cur.execute(f"""UPDATE Users SET Questions = '{question}' WHERE Id = '{user_id}' """)
    else:
        print('Вы уже задавали такой вопрос')

    con.commit()
    con.close()
    # отправка вопросов в БД, у каждого своя ячейка, причем пользователи могут отправлять сразу несколько постов,
    # они будут сохраняться вместе через разделитель


def delete_questions(text):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET Questions = null  WHERE Questions = '{text}' """).fetchall()

    con.commit()
    con.close()
    # после ответа на вопрос пользователя, он удаляется из ячейки, что и делает данная функция


def show_questions():
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Questions FROM Users WHERE Questions IS NOT NULL """).fetchall()
    list_of_questions = []

    for num, el in enumerate(result):
        list_of_questions.append((num + 1, el[0]))

    con.commit()
    con.close()

    return list_of_questions
# эта функция служит для дальнейшего представления вопросов в виде плитки, она возвращает список активных вопросов


def get_id_from_question(text):
    if text != 'No_questions':
        con = sqlite3.connect('Users.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT Id FROM Users WHERE Questions == '{text}' """).fetchall()

        con.commit()
        con.close()

        if result:
            return result[0][0]
        else:
            return 'На данный вопрос уже ответили'
