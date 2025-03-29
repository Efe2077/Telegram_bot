import telebot
import requests
# для получения данных из API
import xlsxwriter
# для записи данных о пользователях в .xlsx - удобный для всех версий вариант представления инф-ции
import os
from dotenv import load_dotenv
import shutil
from telebot import types
from datetime import datetime
from random import choice
from telebot.types import ReplyKeyboardRemove
from for_questions import send_questions, show_questions, get_id_from_question, delete_questions
from add_new import check_admin_status, add_admin, delete_your_admins, add_user, ladmins
from for_yandex_disk import download_file_to_club
from for_file_and_req import slim_shady, count_of_users, ind_grading, group_grading, make_new_folder_from_user, get_clubs
from for_db_tasks import insert_into_db_data, get_data_from_column
while True:
    try:
        # 7050246509:AAHKETNv4k6_Z6FQ37bkCh1QJlqFABpJ2Mo - основной
        # 6996070096:AAHKAAZEvorjnwrd7Fec9kbYzRSt7qTXV7k - Эфе
        # 7072278948:AAHULSz4lWo-FADGtYPvT8zvug3RpySHIFA - Дениса
        load_dotenv()
        BOT = os.getenv('B')
        bot = telebot.TeleBot(BOT)


        GREETINGS = ['Привет', 'Приветствую вас',
                     'Здравствуйте', 'Добрый день'
                     ]
        # Мы сделали вариативные приветствия XD

        GOODBYES = ['До свидания', 'Всего хорошего',
                    'Всего доброго', 'До встречи',
                    'Прощайте', 'Бывай', 'Пока',
                    ]

        consult = show_questions()

        CLUB = ['1 - Содружество',
                '2 - МКСШОР ЮГ',
                '3 - Самбо-70',
                '4 - ФОК Ершово.xlsx',
                '5 - РДДТ Каболоева Б.Е.',
                '6 - ЦСКА',
                '7 - АНО СРС Поволжье',
                '8 - СОК им. Тедеева',
                '9 - Элегия',
                '10 - СШОР Восток',
                '11 - Иска',
                '12 - Старт Тайм',
                '13 - СШ Краснознаменск',
                '14 - Созвездие граций',
                '15 - ГБОУДО Косарева Релеве',
                '16 - СК Переворот',
                '17 - Воробьевы горы']
        TOUR = ['Спортивная весна 2024', 'Маленькая принцесса 2024', 'Весенние звездочки 2024', 'Московская зима 2024', 'Зимняя сказка 2023']


        def start_markup():
            markup = types.InlineKeyboardMarkup(row_width=True)
            link_keyboard1 = types.InlineKeyboardButton(text="канал", url="https://t.me/gymnastkapolechka")
            link_keyboard2 = types.InlineKeyboardButton(text="2 канал", url="https://t.me/rg_child_league")
            link_keyboard3 = types.InlineKeyboardButton(text="3 канал", url="https://t.me/denbug")
            check_keyboard = types.InlineKeyboardButton(text="Проверить", callback_data="check")
            markup.add(link_keyboard1, link_keyboard2, link_keyboard3, check_keyboard)

            return markup
        # Проверка на подписку на тг-каналы проекта - маркап из самих каналов и кнопки "проверить"


        def rename_file(message):
            try:
                if message.text == 'В главное меню':
                    bot.delete_message(message.chat.id, message.message_id - 1)
                    admin(message)
                    return 0
                file_name = message.text
                insert_into_db_data(file_name, 'File_name', message.chat.id)
                insert_into_db_data('sending_file', 'Command', message.chat.id)
                bot.send_message(message.chat.id, f'Прикрепите файл с музыкой (.mp3)')
            except Exception:
                print('Ошибка в rename_file')
                bot.send_message(message.chat.id, 'Ошибка при вводе имени файла')
                admin(message)


        @bot.message_handler(commands=['start', 'hello', 'привет', 'hi'])
        def start(message):
            bot.send_message(message.chat.id, choice(GREETINGS))
            name = message.from_user.first_name

            if name == 'Uniade bot':
                name = message.chat.first_name

            bot.send_message(message.chat.id, name)

            if check(message, message.chat.id) and check_channels_start(message):
                admin(message)
        # команда "/start": приветствие, проверка подписки и в перспективе - авторизация для раздельных лк


        def check(message, chat_id):
            st = bot.get_chat_member(chat_id, user_id=message.chat.id).status
            return st in ["creator", "administrator", "member"]
        # бот, как админ, проверяет наличие статуса в ТГ-каналах


        def check_channels_start(message):
            markup = types.InlineKeyboardMarkup(row_width=True)
            if check(message, "-1001649523664") and check(message, '-1001729713697') and check(message, '-1002142113947'):
                bot.send_message(message.chat.id, "Спасибо за подписку ✨")
                markup.add(admin(message))
            else:
                bot.send_message(message.chat.id, "Подпишись на каналы", reply_markup=start_markup())
        # рекурсивный маркап - до бесконечности, на протяжении всего бота проверяет подписки. Если отпишешься - выдается


        def check_channels(message):
            if check(message, "-1001649523664") and check(message, '-1001729713697') and check(message, '-1002142113947'):
                return True
            else:
                bot.send_message(message.chat.id, "Подпишись на каналы", reply_markup=start_markup())


        def admin(message):
            a = bot.send_message(message.chat.id, 'delete', reply_markup=ReplyKeyboardRemove())
            bot.delete_message(message.chat.id, a.message_id)

            markup = make_main_markup(message)
            bot.send_message(message.chat.id, '\n'
                                              'Если бот не отвечает, '
                                              'попробуйте начать заново: /start или обратиться в поддержку (@di_petrin)')
            bot.send_message(message.chat.id, 'Вы можете выполнить такие функции:', reply_markup=markup)
        # функция вызова главного меню - всему голова


        @bot.message_handler(commands=['bye', 'end', 'пока'])
        def bye(message):
            bot.send_message(message.chat.id, choice(GOODBYES))
        # функция-пасхалка


        @bot.callback_query_handler(func=lambda callback: True)
        def callback_message(callback):
            try:
                if check(callback.message, callback.message.chat.id) and check_channels(callback.message):
                    id_of_user = callback.message.chat.id
                    print(f"{get_data_from_column('Command', id_of_user)} - command by "
                          f"{get_data_from_column('User_name', id_of_user)}")
                    if callback.data == 'add_new_admin':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id,
                                         "Напишите 'Имя пользователя в телеграмме' вашего нового админа",
                                         reply_markup=btn_for_exit()
                                         )
                    # функция добавления нового админа
                    # бот всегда меняет главное меню на функцию во избежание ошибок и для визуального удобства
                    # для выхода в главное меню (далее: ГМ) в клавиатуре создается кнопка "В главное меню"/"Назад"
                        file = open('data/telegram_username.jpg', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        insert_into_db_data('add_admin', 'Command', id_of_user)
                        bot.register_next_step_handler(callback.message, inp_name)
                        # отправка в функцию ввода имени
                    elif callback.data == 'delete_admin':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        insert_into_db_data('delete_admin', 'Command', id_of_user)
                        del_admin(callback.message)
                        # достаем id обратившегося к функции админа (чтобы понять кого он может удаличь) и запускаем функцию
                    elif callback.data == 'our_social_networks':
                        bot.send_message(callback.message.chat.id, 'Вы уже подписаны на наши каналы в Телеграмм'
                                                                   ' и можете узнать многое там')
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('VK', url='https://vk.com/club211067501'))
                        markup.add(
                            types.InlineKeyboardButton('YouTube 🔺', url='https://youtu.be/hVMKtZ6W0n8?si=M9X9P67CwyKHv2HJ'))
                        bot.reply_to(callback.message,
                                     'Но кроме этого, советуем подписаться на наш паблик ВК и посмотреть видео о нас',
                                     reply_markup=markup)
                        # здесь даже без функций - сразу выходит плитка с ссылками67 222`````
                    elif callback.data == 'music':
                        insert_into_db_data('send_file_to_folder', 'Command', id_of_user)
                        bot.edit_message_text(f'Выберете папку:',
                                              reply_markup=show_club(),
                                              chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id)
                    # отправка музыки на Я.Диск, замена плитки ГМ на плитку с выбором папок для добавления музыки
                    # функция напитков - перспектива дальшнейшего развития бота (+ к этому же относиться авторизация)
                    elif callback.data == 'F_A_Q':
                        bot.edit_message_text(f'Вопросы:',
                                              reply_markup=questions(),
                                              chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id)
                    # функция вызова плитки с вопросами
                    # elif callback.data == 'grade':
                    #     bot.delete_message(callback.message.chat.id, callback.message.message_id)
                    #     bot.send_message(callback.message.chat.id, "Введите Фамилию Имя гимнастки:",
                    #                      reply_markup=btn_for_exit())
                    #     bot.register_next_step_handler(callback.message, grade)
                    elif callback.data == 'ind_grade':
                        bot.send_message(callback.message.chat.id, "Введите Фамилию Имя гимнастки:")
                        bot.register_next_step_handler(callback.message, ind_grade)
                    elif callback.data == 'group_grade':
                        bot.send_message(callback.message.chat.id, "Введите название команды или дуэта, "
                                                                   "оценку которого хочешь узнать:")
                        bot.register_next_step_handler(callback.message, group_grade)
                    elif callback.data == 'check':
                        admin(callback.message)
                    # вызов функции вывода оценки из API по ФИО
                    elif callback.data == 'show_questions_from_users':
                        bot.edit_message_text(f'Вопросы от пользователей:',
                                              reply_markup=show_questions_from_users(),
                                              chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id)
                    # вызов плитки вопросов от пользователей
                    elif callback.data == 'send_questions':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id, "Напишите вопрос", reply_markup=btn_for_exit())
                        bot.register_next_step_handler(callback.message, inp_question)
                    # функция обращения от пользователя
                    elif callback.data == 'video_live':
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Трансляция', url='https://vk.com/video-211067501_456239145'))
                        bot.reply_to(callback.message,
                                     'Скорее смотреть!!!',
                                     reply_markup=markup)
                    elif callback.data == 'text_live':
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Репортаж', url='https://vk.com/textlive547685'))
                        bot.reply_to(callback.message,
                                     'Скорее читать!!!',
                                     reply_markup=markup)
                    elif callback.data in TOUR:
                    # в будущем этот общий прием данных для турниров и клубов будет разделен, так как названия
                    # клубов будут отличаться от названий турниров
                        if get_data_from_column('Command', id_of_user) == '6 get_table':
                            bot.delete_message(callback.message.chat.id, callback.message.message_id)
                            f1 = slim_shady(callback.data)
                            bot.send_document(callback.message.chat.id, f1, reply_markup=btn_for_exit())
                    elif callback.data in CLUB:
                        if get_data_from_column('Command', id_of_user) == 'send_file_to_folder':
                            insert_into_db_data(callback.data, 'Your_club', id_of_user)
                            bot.delete_message(callback.message.chat.id, callback.message.message_id)
                            bot.send_message(callback.message.chat.id, 'Введите имя файла:',
                                             reply_markup=btn_for_exit())
                            bot.register_next_step_handler(callback.message, rename_file)
                        # Создание или обращение к существующей папке в Я.Диске для добавления музыки
                    elif callback.data.isdigit():
                        if [i for i in consult if int(callback.data) == i[0]] and callback.data.isdigit():
                            insert_into_db_data('answer_to_question', 'Command', id_of_user)
                            bot.delete_message(callback.message.chat.id, callback.message.message_id)
                            bot.send_message(callback.message.chat.id, f"Вы выбрали '{consult[int(callback.data) - 1][1]}'")
                            insert_into_db_data(consult[int(callback.data) - 1][1], 'Printed_work', id_of_user)
                            bot.register_next_step_handler(callback.message, answer)
                        # ответы на вопросы от  elif callback.data == 'group_grade
                        #  elif callback.data == 'group_gradeпользователей
                    elif callback.data == 'show_count_of_users':
                        c_of_users = count_of_users()
                        bot.send_message(callback.message.chat.id, c_of_users)
                        # вызов функции обращения к API сайта, а именно получения кол-ва открытых кабинетов
                    elif callback.data == 'table':
                        insert_into_db_data('get_table', 'Command', id_of_user)
                        bot.edit_message_text(f'Выберите интересующий турнир:',
                                              reply_markup=change_on_table(),
                                              chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id)
                        # Создание плиток с выбором турнира, по которому выгрузить заявки и создать EXCEl
                    elif callback.data == 'qw_1':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        file = open('data/checkroom0.jpg', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id,
                                         'Войдя через главный вход, проходите через турникет и заворачиваете направо')
                        file = open('data/checkroom1.jpg', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id, 'проходите по коридору вперед')
                        file = open('data/checkroom2.jpg', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id, 'поворачиваете налево и входите в раздевалку, вы на месте!',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_2':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        file = open('data/rating1.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
                        bot.send_message(callback.message.chat.id,
                                         'Зарегистрироваться на сайте (если еще этого не сделали), в профиле выбрать "достижения"',
                                         reply_markup=markup)
                        file = open('data/rating2.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id,
                                         'В разделе достижения будет указано значения рейтинга (твой рейтинг) и достижения',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_3':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Смотреть!', callback_data='grade'))
                        bot.send_message(callback.message.chat.id,
                                         'Вы можете посмотреть оценки участниц прошлого федерального этапа',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_4':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id, 'Фото будут доступны на сайте ниже с 16 апреля')
                        file = open('data/photo_qr.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file, reply_markup=btn_for_questions())
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Заказать', url='http://kondakov.online/order.html'))
                        bot.send_message(callback.message.chat.id,
                                         'Сайт с фотографиями',
                                         reply_markup=markup)
                    elif callback.data == 'qw_5':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id, 'ответ 5', reply_markup=btn_for_questions())
                    elif callback.data == 'qw_6':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id,
                                         'Чтобы судьи понимали тайминг упражнения, соответствующий правилам!',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_7':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton(
                                'Скорее смотреть!!!', url='https://vk.com/textlive547685'))
                        bot.send_message(callback.message.chat.id,
                                         'Подайте заявку на вступление в сообщество.',
                                         reply_markup=markup)
                        bot.send_message(callback.message.chat.id, 'Когда она будет принята, Вы сможете узнать в репортаже',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_8':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton(
                                'Скорее смотреть!!!', url='https://vk.com/textlive547685'))
                        bot.send_message(callback.message.chat.id,
                                         'Подайте заявку на вступление в сообщество.',
                                         reply_markup=markup)
                        bot.send_message(callback.message.chat.id,
                                         'Когда она будет принята, Вы сможете увидеть долгожданные выступления',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_9':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        file = open('data/online1.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
                        bot.send_message(callback.message.chat.id,
                                         'Зарегистрироваться на сайте (если еще этого не сделали), '
                                         'в профиле выбрать "подать заявку"',
                                         reply_markup=markup)
                        file = open('data/online2.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id, 'При оплате выбрать "онлайн"',
                                         reply_markup=btn_for_questions())
                    elif callback.data == 'qw_10':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        file = open('data/photo1.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        markup = types.InlineKeyboardMarkup()
                        markup.add(
                            types.InlineKeyboardButton('Перейти в профиль/зарегистрироваться', url='https://uniade.world/profile'))
                        bot.send_message(callback.message.chat.id,
                                         'Зарегистрироваться на сайте (если еще этого не сделали), '
                                         'в профиле выбрать "загрузить фото для турнира"',
                                         reply_markup=markup)
                        file = open('data/photo2.png', 'rb')
                        bot.send_photo(callback.message.chat.id, file)
                        bot.send_message(callback.message.chat.id,
                                         'Далее нажмите "Загрузить фото"', reply_markup=btn_for_questions())
                    elif callback.data == 'qw_11':
                        bot.delete_message(callback.message.chat.id, callback.message.message_id)
                        bot.send_message(callback.message.chat.id, 'Справа от входа в арку находится стол dj, '
                                                                   'именно этому харизматичному мужчине нужно сдать флешку XD')
                        file = open('data/dj.jpg', 'rb')
                        bot.send_photo(callback.message.chat.id, file, reply_markup=btn_for_questions())
                    #Прием всех вопросов из плитки вопросов и вызов соответствующих ответов
                    elif callback.data == 'qw_quit':
                        bot.edit_message_text(f'Вы можете выполнить такие функции:',
                                              reply_markup=make_main_markup(callback.message),
                                              chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id)
                    #выход в главное мен
            except Exception:
                admin(callback.message)
                bot.send_message(callback.message.chat.id, 'Что-то пошло не так, попробуйте ещераз')


        @bot.message_handler(content_types=['text'])
        # прием текстовых вводов пользователя и соответствующие функции
        def func(message):
            if message.text == "✅ Да":
                user_name = get_data_from_column('Name', message.chat.id)
                name_of_smb = get_data_from_column('Name_of_smb', message.chat.id)
                if get_data_from_column('Command', message.chat.id) == 'add_admin':
                    mess = add_admin(user_name, name_of_smb)
                    bot.send_message(message.chat.id, mess, reply_markup=btn_for_exit())

                elif get_data_from_column('Command', message.chat.id) == 'delete_admin':
                    mess = delete_your_admins(user_name, name_of_smb)
                    bot.send_message(message.chat.id, mess, reply_markup=btn_for_exit())

            elif message.text == "❌ Нет":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                btn1 = types.KeyboardButton('Написать еще раз')
                btn2 = types.KeyboardButton('В главное меню')
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, 'Выберете:', reply_markup=markup)

            elif message.text == 'Написать еще раз':
                bot.send_message(message.chat.id, "Повторите")
                bot.register_next_step_handler(message, inp_name)

            elif message.text == 'В главное меню' or message.text == 'Назад':
                admin(message)

            elif message.text == 'К вопросам':
                bot.send_message(message.chat.id, 'Вопросы:', reply_markup=questions())


        @bot.message_handler(content_types=['photo'])
        # прием фото, чтобы можно было через бота получить какую-то обратную связь на них
        def get_photo(message):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Перейти в вк', url='https://vk.com/rg_child_league'))
            bot.reply_to(message, 'Здорово! Не хотите ли Вы предложить это фото для поста в канале?', reply_markup=markup)


        @bot.message_handler(content_types=['audio'])
        def send_audio_into_folder(message):
            try:
                if get_data_from_column('Command', message.chat.id) == 'sending_file':
                    # Получаем информацию о файле
                    file_info = bot.get_file(message.audio.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)  # Получаем бинарные данные файла

                    file_name = get_data_from_column('File_name', message.chat.id)
                    your_club = get_data_from_column('Your_club', message.chat.id)

                    # Загружаем напрямую на Яндекс.Диск
                    success = download_file_to_club(your_club, file_name, downloaded_file)

                    if not success:
                        bot.send_message(message.chat.id, 'Файл с таким названием уже существует или произошла ошибка\n'
                                                          'Поменяйте название файла и прикрепите его повторно')
                    else:
                        bot.send_message(message.chat.id, 'Файл успешно прикреплен', reply_markup=btn_for_exit())

                    # Очистка значений
                    insert_into_db_data('', 'File_name', message.chat.id)
                    insert_into_db_data('send_file_to_folder', 'Command', message.chat.id)

            except Exception as e:
                print(f'Ошибка при обработке аудио: {e}')
                bot.send_message(message.chat.id, 'Произошла ошибка при обработке файла', reply_markup=admin(message))


        # Ввод фамилии и имени пользователя:
        def inp_folder(message):
            try:
                if message.text == 'В главное меню':
                    bot.delete_message(message.chat.id, message.message_id - 1)
                    admin(message)
                    return 0
                text = message.text
                text = text.capitalize()
                insert_into_db_data(text, 'Fio', message.chat.id)
                bot.send_message(message.chat.id, f'Ваша папка: \n{text}')
                insert_into_db_data('sending_file', 'Command', message.chat.id)
                bot.send_message(message.chat.id, f'Прикрепите файл с музыкой (.mp3)')
            except Exception:
                print('Ошибка в inp_folder')
                bot.send_message(message.chat.id,'Ошибка при вводе имени папки')
                admin(message)
        # Ввод имени админа:

        def inp_name(message):
            try:
                if message.text == 'В главное меню':
                    bot.delete_message(message.chat.id, message.message_id - 1)
                    bot.delete_message(message.chat.id, message.message_id - 2)
                    admin(message)
                    return 0
                text = message.text
                insert_into_db_data(text, 'Name_of_smb', message.chat.id)
                bot.send_message(message.chat.id, f'Тако`е имя: {text}?')
                yes_or_no(message)
            except Exception:
                print('Ошибка в имени inp_name')


        # Клавиатура для подтверждения:
        def yes_or_no(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
            btn1 = types.KeyboardButton('✅ Да')
            btn2 = types.KeyboardButton('❌ Нет')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Да/Нет', reply_markup=markup)


        #удаление админов:
        def del_admin(message):
            if message.text == 'В главное меню':
                bot.delete_message(message.chat.id, message.message_id - 1)
                bot.delete_message(message.chat.id, message.message_id - 2)
                admin(message)
                return 0
            bot.send_message(message.chat.id, 'Внимание! Вы можете удалить только тех админов, которых вы добавляли')
            bot.send_message(message.chat.id, "Напишите 'Имя пользователя в телеграмме' админа",
                             reply_markup=btn_for_exit())
            bot.register_next_step_handler(message, inp_name)
        # Ввод вопросов:
        def inp_question(message):
            try:
                if message.text == 'В главное меню':
                    admin(message)
                    return 0
                question_from_user = message.text
                bot.send_message(message.chat.id, f"Ваш вопрос:\n{question_from_user}", reply_markup=btn_for_exit())
                now = datetime.now().strftime('%m-%d %H:%M')
                send_questions(message.chat.id, str(now) + ': ' + question_from_user)
                admin_list = ladmins()
                for i in admin_list:
                    bot.send_message(int(i), 'Новый вопрос от пользователя!!!')
                # Уведомление всех админов о вопросе
            except Exception:
                print('Ошибка в вопросе inp_question')
                bot.send_message(message.chat.id, 'Ошибка в вопросе!!!')


        #Ответ от админа на вопросы пользователя:
        def answer(message):
            text = message.text
            bot.send_message(message.chat.id, f'Ваш ответ: {text}')
            printed_work = get_data_from_column('Printed_work', message.chat.id)
            print(printed_work)
            send_answer_from_admin(message, get_id_from_question(printed_work), text)


        # Плитка с выбором из папок:
        def show_club():
            markup = types.InlineKeyboardMarkup()
            for club in CLUB:
                btn = types.InlineKeyboardButton(club, callback_data=club)
                markup.add(btn)

            exit_btn = types.InlineKeyboardButton('Выйти', callback_data='qw_quit')
            markup.add(exit_btn)

            return markup


        # Функция для вывода оценки:
        def ind_grade(message):
            if message.text == 'В главное меню':
                bot.delete_message(message.chat.id, message.message_id - 1)
                admin(message)
                return 0
            text = message.text
            res = ind_grading(text)
            bot.send_message(message.chat.id, res, reply_markup=btn_for_exit())


        def group_grade(message):
            if message.text == 'В главное меню':
                bot.delete_message(message.chat.id, message.message_id - 1)
                admin(message)
                return 0
            text = message.text
            res = group_grading(text)
            bot.send_message(message.chat.id, res, reply_markup=btn_for_exit())


        # вопросы от пользоваетелей (плитка):
        def show_questions_from_users():
            global consult
            markup = types.InlineKeyboardMarkup()
            consult = show_questions()
            for i in consult:
                markup.add(types.InlineKeyboardButton(f'{i[1]}', callback_data=i[0]))
            ret = types.InlineKeyboardButton(f'Выйти', callback_data='qw_quit')
            markup.add(ret)

            return markup


        def send_answer_from_admin(message, id_of_user, text):
            printed_work = get_data_from_column('Questions', id_of_user)
            delete_questions(printed_work)
            bot.send_message(id_of_user, f'Ответ от админа: {text}')
            admin(message)


        # Выводит кнопки с названием Турниров
        def change_on_table():
            markup = types.InlineKeyboardMarkup()
            for i in TOUR:
                markup.add(types.InlineKeyboardButton(f'{i}', callback_data=i))
            ret = types.InlineKeyboardButton(f'Выйти', callback_data='qw_quit')
            markup.add(ret)

            return markup


        # Главные кнопки
        def make_main_markup(message):
            name, name2, id_of_user = message.chat.username, message.chat.first_name, message.chat.id

            admin_status = check_admin_status(name)  # проверка статуса админа
            add_user(name, name2, id_of_user)  # Добавление нового пользователя

            markup = types.InlineKeyboardMarkup()
            # btn2 = types.InlineKeyboardButton('Групповая оценка', callback_data='group_grade')
            # btn3 = types.InlineKeyboardButton('Индивид. оценка', callback_data='ind_grade')
            # markup.row(btn2)
            # markup.row(btn3)
            btn4 = types.InlineKeyboardButton('Загрузить музыку', callback_data='music')
            markup.row(btn4)
            btn6 = types.InlineKeyboardButton('Обратиться к организаторам', callback_data='send_questions')
            markup.row(btn6)
            # btn7 = types.InlineKeyboardButton('ЧаВо⁉️', callback_data='F_A_Q')
            btn8 = types.InlineKeyboardButton('О нас', callback_data='our_social_networks')
            markup.row(btn8)
            # btn9 = types.InlineKeyboardButton('Видео-live', callback_data='video_live')
            # btn10 = types.InlineKeyboardButton('Репортаж', callback_data='text_live')
            # markup.row(btn9, btn10)
            if admin_status:
                btn_for_admin1 = types.InlineKeyboardButton('Добавить админа', callback_data='add_new_admin')
                markup.row(btn_for_admin1)
                btn_for_admin2 = types.InlineKeyboardButton('Удалить админа', callback_data='delete_admin')
                markup.row(btn_for_admin2)
                btn_for_admin3 = types.InlineKeyboardButton('Вопросы от пользователей',
                                                            callback_data='show_questions_from_users')
                markup.row(btn_for_admin3)
                btn_for_admin3 = types.InlineKeyboardButton('Количество пользователей', callback_data='show_count_of_users')
                markup.row(btn_for_admin3)
                btn_for_admin4 = types.InlineKeyboardButton('Таблица участников', callback_data='table')
                markup.row(btn_for_admin4)

            return markup


        # Кнопки с вопросами
        def questions():
            markup2 = types.InlineKeyboardMarkup()
            markup2.add(types.InlineKeyboardButton('Где раздевалка?', callback_data='qw_1'))  # фото-ряд
            markup2.add(
                types.InlineKeyboardButton('Где найти рейтинг Юниады?', callback_data='qw_2'))  # https://uniade.world/profile
            markup2.add(types.InlineKeyboardButton('Как посмотреть оценки?',
                                                   callback_data='qw_3'))
            markup2.add(types.InlineKeyboardButton('Как заказать фотографии?', callback_data='qw_4'))
            markup2.add(types.InlineKeyboardButton('Как найти визажиста на турнире?', callback_data='qw_5'))
            markup2.add(types.InlineKeyboardButton('Зачем нужен гонг?', callback_data='qw_6'))
            markup2.add(types.InlineKeyboardButton('Какой поток выступает?', callback_data='qw_7'))
            markup2.add(types.InlineKeyboardButton('Как посмотреть трансляцию?', callback_data='qw_8'))
            markup2.add(types.InlineKeyboardButton('Как поучаствовать в Юниаде онлайн?', callback_data='qw_9'))
            markup2.add(types.InlineKeyboardButton('Как загрузить фото, чтобы попасть на экран?', callback_data='qw_10'))
            markup2.add(types.InlineKeyboardButton('Куда сдавать музыку?', callback_data='qw_11'))
            markup2.add(types.InlineKeyboardButton('выйти', callback_data='qw_quit'))
            return markup2


        # Кнопка для выхода
        def btn_for_exit():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
            btn = types.KeyboardButton('В главное меню')
            markup.add(btn)

            return markup


        def btn_for_questions():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
            btn = types.KeyboardButton('К вопросам')
            markup.add(btn)

            return markup


        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except Exception:
        print('Ну заново, че)')