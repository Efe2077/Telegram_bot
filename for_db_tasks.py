import sqlite3


def get_data_from_column(column, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT {column} FROM Users WHERE Id = '{user_id}' """).fetchall()

    con.commit()
    con.close()

    return result[0][0]


def insert_into_db_data(thing, column, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()

    cur.execute(f"""UPDATE Users SET '{column}' = '{thing}' WHERE Id = '{user_id}' """).fetchall()

    con.commit()
    con.close()


# 1267835682
