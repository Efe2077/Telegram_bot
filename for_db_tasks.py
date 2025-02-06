import sqlite3


def get_data_from_column(column, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT {column} FROM Users WHERE Id = '{user_id}' """).fetchall()

    con.commit()
    con.close()
    if result:
        return result[0][0]
    else:
        return 'Ошибка'


def insert_into_db_data(thing, column, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()

    query = f"UPDATE Users SET {column} = ? WHERE Id = ?"
    cur.execute(query, (thing, user_id))

    con.commit()
    con.close()


# 1267835682
