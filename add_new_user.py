import sqlite3


def add_user(user_name, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name, id FROM Users WHERE Id = ?""", (user_id, )).fetchall()
    if result:
        print(result)
    else:
        cur.execute(f"""INSERT INTO Users(Name, Id) VALUES('{user_name}', {user_id})""").fetchall()
        print(f"""
        Новый пользователь зарегистрирован:
            {user_name}
            {user_id}
               """)
    con.commit()
    con.close()

    con = sqlite3.connect('Admins.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name, id FROM Admins WHERE Id = ?""", (user_id,)).fetchall()
    if result:
        ADMIN = True
    else:
        ADMIN = False

    return ADMIN


