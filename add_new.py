import sqlite3


def add_user(user_name, user_name2, user_id):
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Name, Id FROM Users WHERE Id = '{user_id}' """).fetchall()
    if not result:
        cur.execute(f"""INSERT INTO Users(Name, Id, Questions, User_name, Command) VALUES('{user_name}', 
                        {user_id}, null, '{user_name2}', null)""").fetchall()
        print(f"""
        Новый пользователь зарегистрирован:
            {user_name}
            {user_id}
               """)

    con.commit()
    con.close()


def check_admin_status(user_name):
    con = sqlite3.connect('Admins.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT Name FROM Admins WHERE Name = '{user_name}' """).fetchall()

    con.commit()
    con.close()

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
    result = cur.execute(f"""SELECT Name from Admins WHERE Name = '{admin_name}' """).fetchall()

    if result:
        note = 'Данный пользователь уже является админом'
        return note
    else:
        result2 = cur.execute(f"""SELECT Added_admin from Admins WHERE Name = '{your_name}' """).fetchall()

        if not result2:
            answer = admin_name
        else:
            yours_admins = result2[0][0]
            answer = yours_admins + ' ' + admin_name
        cur.execute(f"""INSERT INTO Admins(Name, Added_admin) VALUES('{admin_name}', 'Not')""").fetchall()
        cur.execute(f"""UPDATE Admins SET Added_admin = '{answer}'
                        WHERE Name = '{your_name}'""").fetchall()
        note = 'Админ добавлен'

    con.commit()
    con.close()

    return note


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
        note = 'У вас нет добавленных админов'
        return note

    if not (name in list_of_yours):
        note = 'Вы не можете удалить данного админа, потому что вы его не добавляли'
        return note

    # Удаление админа

    his = ''

    his_admins = cur.execute(f"""SELECT Added_admin from Admins WHERE Name = ?""", (name, )).fetchall()
    if his_admins[0][0] != 'Not':
        his = his_admins[0][0]

    cur.execute(f"""DELETE FROM Admins WHERE Name = '{name}'""")

    # Удаление добавленного админа у тебя в списке
    beta_list = ' '.join(list_of_yours)
    upd_list = ' '.join([i.strip() for i in beta_list.split(name) if i])
    upd_list = upd_list.strip()

    if not upd_list:
        upd_list = 'Not'

    if his:
        upd_list += ' ' + his

    cur.execute(f"""UPDATE Admins SET Added_admin = '{upd_list}' WHERE Name = '{your_name}'""")

    note = 'Админ удален'

    con.commit()
    con.close()

    return note


# ДЗ
# Сделать круто!!!!!!!!!!!!

def ladmins():
    con = sqlite3.connect('Admins.db')
    cur = con.cursor()
    result0 = cur.execute(f"""SELECT Name FROM Admins""").fetchall()
    con = sqlite3.connect('Users.db')
    cur = con.cursor()
    result1 = cur.execute(f"""SELECT ID FROM Users WHERE Name IN ('EfeFe4', 'di_petrin', 'Dinamit6663_1', 'Tester', 'bgalkin')""").fetchall()
    result2 = [x[0] for x in result1]
    return result2