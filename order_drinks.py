from datetime import datetime
from telebot import types
from for_db_tasks import insert_into_db_data, get_data_from_column
from add_new import ladmins

# Глобальный словарь для хранения заказов в процессе создания
user_orders = {}

# Подтипы для чая и кофе
COFFEE_TYPES = ["Латте", "Капучино", "Эспрессо"]
TEA_TYPES = ["Черный", "Зеленый"]


def start_order(message, bot):
    """Начало заказа."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Кофе", callback_data="ordy_coffee"),
        types.InlineKeyboardButton(text="Чай", callback_data="ordy_tea"),
        types.InlineKeyboardButton(text="Молоко", callback_data="ordy_milk"),
        types.InlineKeyboardButton(text="Вода", callback_data="ordy_water"),
        types.InlineKeyboardButton(text="Кипяток", callback_data="ordy_boiled_water"),
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Что вы хотите заказать?", reply_markup=markup)


def process_drink_choice(callback_query, bot):
    """Обработка выбора напитка."""
    query = callback_query
    chat_id = query.message.chat.id
    data = query.data.split("_")[1]
    if data not in ["coffee", "tea", "milk", "water", "boiled_water"]:
        bot.answer_callback_query(query.id, "Произошла ошибка. Пожалуйста, попробуйте выбрать напиток снова.")
        return start_order(query.message, bot)

    user_orders[chat_id] = {"drinks": [], "location": None, "status": "оформлен"}

    if data == "coffee":
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(text=coffee_type, callback_data=f"coffee_{coffee_type}") for coffee_type in COFFEE_TYPES]
        markup.add(*buttons)
        bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="Какой кофе вы хотите?", reply_markup=markup)
    elif data == "tea":
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(text=tea_type, callback_data=f"tea_{tea_type}") for tea_type in TEA_TYPES]
        markup.add(*buttons)
        bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="Какой чай вы хотите?", reply_markup=markup)
    elif data == "milk":
        user_orders[chat_id]["drinks"].append({"type": "Молоко", "subtype": None, "sugar": "Без сахара"})
        ask_for_more(query.message, bot)
    elif data == "water":
        user_orders[chat_id]["drinks"].append({"type": "Вода", "subtype": None, "sugar": "Без сахара"})
        ask_for_more(query.message, bot)
    elif data == "boiled_water":
        user_orders[chat_id]["drinks"].append({"type": "Кипяток", "subtype": None, "sugar": "Без сахара"})
        ask_for_more(query.message, bot)


def process_subtype_choice(callback_query, bot):
    """Обработка выбора подтипа напитка."""
    try:
        query = callback_query
        chat_id = query.message.chat.id  # Получаем chat_id из callback_query
        data = query.data.split("_")
        drink_type = data[0]  # Тип напитка (coffee или tea)
        subtype = "_".join(data[1:])  # Подтип напитка (например, Латте, Черный)

        # Проверяем, что подтип допустим
        if (drink_type == "coffee" and subtype not in COFFEE_TYPES) or (drink_type == "tea" and subtype not in TEA_TYPES):
            bot.answer_callback_query(query.id, "Произошла ошибка. Пожалуйста, попробуйте выбрать подтип снова.")
            return

        # Добавляем выбранный подтип в заказ
        if chat_id not in user_orders:
            user_orders[chat_id] = {"drinks": [], "location": None, "status": "оформлен"}
        user_orders[chat_id]["drinks"].append({"type": drink_type.capitalize(), "subtype": subtype, "sugar": None})

        # Переходим к выбору сахара
        ask_for_sugar(query.message, bot)  # Используем query.message, а не query.message.message
    except Exception as e:
        print(f"Ошибка в process_subtype_choice: {e}")
        bot.answer_callback_query(query.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


def ask_for_sugar(callback_query, bot):
    """Запрос на добавление сахара."""
    query = callback_query
    chat_id = query.message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Без сахара", callback_data="sugar_none"),
        types.InlineKeyboardButton(text="1 ложка", callback_data="sugar_1"),
        types.InlineKeyboardButton(text="2 ложки", callback_data="sugar_2"),
        types.InlineKeyboardButton(text="3 ложки", callback_data="sugar_3"),
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, "Сколько сахара добавить?", reply_markup=markup)


def process_sugar_choice(callback_query, bot):
    """Обработка выбора сахара."""
    query = callback_query
    chat_id = query.message.chat.id
    data = query.data.split("_")[1]
    user_orders[chat_id]["drinks"][-1]["sugar"] = data if data != "none" else "Без сахара"
    ask_for_more(query.message, bot)


def ask_for_more(callback_query, bot):
    """Запрос на добавление еще одного напитка или завершение заказа."""
    query = callback_query
    chat_id = query.message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Повторить", callback_data="repeat"),
        types.InlineKeyboardButton(text="Новый напиток", callback_data="new_drink"),
        types.InlineKeyboardButton(text="Готово", callback_data="finish"),
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, "Что дальше?", reply_markup=markup)

def process_more_choice(callback_query, bot):
    """Обработка выбора: повторить, новый напиток или завершить."""
    query = callback_query
    chat_id = query.message.chat.id
    data = query.data
    if data == "repeat":
        last_drink = user_orders[chat_id]["drinks"][-1]
        user_orders[chat_id]["drinks"].append(last_drink)
        ask_for_more(query.message, bot)
    elif data == "new_drink":
        start_order(query.message, bot)
    elif data == "finish":
        ask_delivery_location(query.message, bot)
    else:
        bot.answer_callback_query(query.id, "Произошла ошибка. Пожалуйста, попробуйте выбрать вариант снова.")
        ask_for_more(query.message, bot)

def ask_delivery_location(callback_query, bot):
    """Запрос места доставки."""
    query = callback_query
    chat_id = query.message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    locations = ["Стол Главного Судьи", "А1", "А2", "А3", "А4", "Е1", "Е2", "Е3", "Е4", "DB1", "DB2", "DA1", "DA2"]
    buttons = [types.InlineKeyboardButton(text=location, callback_data=f"location_{location}") for location in locations]
    markup.add(*buttons)
    bot.send_message(chat_id, "Куда доставить заказ?", reply_markup=markup)

def process_delivery_location(callback_query, bot):
    """Обработка выбора места доставки."""
    query = callback_query
    chat_id = query.message.chat.id
    location = query.data.split("_")[1]
    user_orders[chat_id]["location"] = location
    confirm_order(query.message, bot)

def confirm_order(callback_query, bot):
    """Подтверждение заказа."""
    query = callback_query
    chat_id = query.message.chat.id
    order = user_orders[chat_id]
    order["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order["user_id"] = chat_id

    # Форматируем заказ для отображения
    order_text = format_order_text(order)
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order"),
        types.InlineKeyboardButton(text="Отменить", callback_data="cancel_order"),
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, f"Ваш заказ:\n{order_text}\nПодтвердите заказ:", reply_markup=markup)

def process_confirmation(callback_query, bot):
    """Обработка подтверждения заказа."""
    query = callback_query
    chat_id = query.message.chat.id
    data = query.data
    if data == "confirm_order":
        # Сохраняем заказ в базу данных
        save_order_to_db(chat_id, user_orders[chat_id])
        # Уведомляем администраторов
        notify_admins(bot, user_orders[chat_id])
        bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="Заказ подтвержден и отправлен на обработку.")
    elif data == "cancel_order":
        bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text="Ваш заказ был отменен.", reply_markup=None)
        del user_orders[chat_id]

def save_order_to_db(chat_id, order):
    """Сохраняет заказ в базу данных."""
    current_orders = get_data_from_column("Orders", chat_id)
    if not current_orders:
        current_orders = []
    else:
        current_orders = eval(current_orders)

    current_orders.append(order)
    insert_into_db_data(str(current_orders), "Orders", chat_id)

def format_order_text(order):
    """Форматирует заказ в читаемый вид."""
    drinks_text = "\n".join(
        [f"{drink['type']} ({drink.get('subtype', '')}, сахар: {drink.get('sugar', 'без сахара')}" for drink in
         order["drinks"]])
    return (
        f"Время заказа: {order['time']}\n"
        f"Место доставки: {order['location']}\n"
        f"Напитки:\n{drinks_text}\n"
        f"Статус: {order['status']}"
    )

def notify_admins(bot, order):
    """Уведомляет администраторов о новом заказе."""
    admin_ids = ladmins()  # Получение списка администраторов
    for admin_id in admin_ids:
        bot.send_message(admin_id, f"Поступил новый заказ:\n\n{format_order_text(order)}")