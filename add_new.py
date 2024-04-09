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
    result = cur.execute(f"""SELECT Name FROM Admins WHERE Name = ?""",
                         (user_name, )).fetchall()
    if result:
        ADMIN = True
    else:
        ADMIN = False

    return ADMIN


def add_admin(your_name, admin_name):
    if not admin_name:
        return 0
    elif admin_name[0] == '@':
        admin_name = admin_name[1:]

    con = sqlite3.connect('Admins.db')
    cur = con.cursor()

   result = cur.execute(f"""SELECT Name from Admins WHERE Name = ?""", (admin_name, )).fetchall()

    if result:
        print('Данный пользователь уже является админом')
    else:
        result2 = cur.execute(f"""SELECT Added_admin from Admins WHERE Name = ?""", (your_name,)).fetchall()
        yours_admins = result2[0][0]
        if yours_admins == 'Not':
            answer = admin_name
        else:
            answer = yours_admins + ' ' + admin_name
        cur.execute(f"""INSERT INTO Admins(Name, Added_admin) VALUES('{admin_name}', 'Not')""").fetchall()
        cur.execute(f"""UPDATE Admins SET Added_admin = '{answer}'
                        WHERE Name = '{your_name}'""").fetchall()
        print('Админ добавлен')

    con.commit()
    con.close()


def delete_your_admins(your_name, name):
    if not name:
        return 0
    elif name[0] == '@':
        name = name[1:]

    con = sqlite3.connect('Admins.db')
    cur = con.cursor()

    result = cur.execute(f"""SELECT Added_admin from Admins WHERE Name = ?""", (your_name, )).fetchall()

    if result[0][0] is not None:
        list_of_yours = [i[0] for i in result][0].split()
    else:
        print('У вас нет добавленных админов')
        return

    if not (name in list_of_yours):
        print('Вы не можете удалить данного админа, потому что вы его не добавляли')
        return 0

    # Удаление админа

    cur.execute(f"""DELETE FROM Admins WHERE Name = '{name}'""")

    # Удаление добавленного админа у тебя в списке
    beta_list = ' '.join(list_of_yours)
    upd_list = ' '.join([i.strip() for i in beta_list.split(name) if i])
    upd_list = upd_list.strip()

    if not upd_list:
        upd_list = 'Not'

    cur.execute(f"""UPDATE Admins SET Added_admin = '{upd_list}' WHERE Name = '{your_name}'""")

    print('Админ удален')

    con.commit()
    con.close()


# add_admin('EfeFe4', 'Me')
