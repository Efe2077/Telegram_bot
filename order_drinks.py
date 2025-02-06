from datetime import datetime
from telebot import types
from for_db_tasks import insert_into_db_data, get_data_from_column
from add_new import ladmins

# Глобальный словарь для хранения заказов в процессе создания
user_orders = {}

# Подтипы для чая и кофе
COFFEE_TYPES = ["Латте", "Капучино", "Эспрессо"]
TEA_TYPES = ["Черный", "Зеленый", "Фруктовый"]


def start_order(message, bot):
    """Начало заказа."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Кофе", "Чай", "Молоко", "Вода", "Кипяток")
    bot.send_message(message.chat.id, "Что вы хотите заказать?", reply_markup=markup)
    bot.register_next_step_handler(message, process_drink_choice, bot)


def process_drink_choice(message, bot):
    """Обработка выбора напитка."""
    drink = message.text
    if drink not in ["Кофе", "Чай", "Молоко", "Вода", "Кипяток"]:
        bot.send_message(message.chat.id, "Пожалуйста, выберите напиток из списка.")
        return start_order(message, bot)

    user_orders[message.chat.id] = {"drinks": [], "location": None, "status": "оформлен"}

    if drink == "Кофе":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for coffee_type in COFFEE_TYPES:
            markup.add(coffee_type)
        bot.send_message(message.chat.id, "Какой кофе вы хотите?", reply_markup=markup)
        bot.register_next_step_handler(message, process_subtype_choice, bot, drink)
    elif drink == "Чай":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for tea_type in TEA_TYPES:
            markup.add(tea_type)
        bot.send_message(message.chat.id, "Какой чай вы хотите?", reply_markup=markup)
        bot.register_next_step_handler(message, process_subtype_choice, bot, drink)
    else:
        user_orders[message.chat.id]["drinks"].append({"type": drink, "subtype": None, "sugar": "Без сахара"})
        ask_for_more(message, bot)


def process_subtype_choice(message, bot, drink):
    """Обработка выбора подтипа напитка."""
    subtype = message.text
    if (drink == "Кофе" and subtype not in COFFEE_TYPES) or (drink == "Чай" and subtype not in TEA_TYPES):
        bot.send_message(message.chat.id, "Пожалуйста, выберите подтип из списка.")
        return process_drink_choice(message, bot)

    user_orders[message.chat.id]["drinks"].append({"type": drink, "subtype": subtype, "sugar": None})
    ask_for_sugar(message, bot)


def ask_for_sugar(message, bot):
    """Запрос на добавление сахара."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Без сахара", "1 ложка", "2 ложки", "3 ложки")
    bot.send_message(message.chat.id, "Сколько сахара добавить?", reply_markup=markup)
    bot.register_next_step_handler(message, process_sugar_choice, bot)


def process_sugar_choice(message, bot):
    """Обработка выбора сахара."""
    sugar = message.text
    user_orders[message.chat.id]["drinks"][-1]["sugar"] = sugar
    ask_for_more(message, bot)


def ask_for_more(message, bot):
    """Запрос на добавление еще одного напитка или завершение заказа."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Повторить", "Новый напиток", "Готово")
    bot.send_message(message.chat.id, "Что дальше?", reply_markup=markup)
    bot.register_next_step_handler(message, process_more_choice, bot)


def process_more_choice(message, bot):
    """Обработка выбора: повторить, новый напиток или завершить."""
    choice = message.text
    if choice == "Повторить":
        last_drink = user_orders[message.chat.id]["drinks"][-1]
        user_orders[message.chat.id]["drinks"].append(last_drink)
        ask_for_more(message, bot)
    elif choice == "Новый напиток":
        start_order(message, bot)
    elif choice == "Готово":
        ask_delivery_location(message, bot)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите из предложенных вариантов.")
        ask_for_more(message, bot)


def ask_delivery_location(message, bot):
    """Запрос места доставки."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    locations = ["Стол Главного Судьи", "А1", "А2", "А3", "А4", "Е1", "Е2", "Е3", "Е4", "DB1", "DB2", "DA1", "DA2"]
    for location in locations:
        markup.add(location)
    bot.send_message(message.chat.id, "Куда доставить заказ?", reply_markup=markup)
    bot.register_next_step_handler(message, process_delivery_location, bot)


def process_delivery_location(message, bot):
    """Обработка выбора места доставки."""
    location = message.text
    user_orders[message.chat.id]["location"] = location
    confirm_order(message, bot)


def confirm_order(message, bot):
    """Подтверждение заказа."""
    order = user_orders[message.chat.id]
    order["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order["user_id"] = message.chat.id

    # Форматируем заказ для отображения
    order_text = format_order_text(order)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Подтвердить заказ", "Отменить")
    bot.send_message(message.chat.id, f"Ваш заказ:\n{order_text}\nПодтвердите заказ:", reply_markup=markup)
    bot.register_next_step_handler(message, process_confirmation, bot, order)


def process_confirmation(message, bot, order):
    """Обработка подтверждения заказа."""
    if message.text == "Подтвердить заказ":
        # Сохраняем заказ в базу данных
        save_order_to_db(message.chat.id, order)
        # Уведомляем админов
        notify_admins(bot, order)
        bot.send_message(message.chat.id, "Заказ подтвержден и отправлен на обработку.")
    else:
        bot.send_message(message.chat.id, "Заказ отменен.")


def save_order_to_db(user_id, order):
    """Сохраняет заказ в базу данных."""
    current_orders = get_data_from_column("Orders", user_id)
    if not current_orders:
        current_orders = []
    else:
        current_orders = eval(current_orders)

    current_orders.append(order)
    insert_into_db_data(str(current_orders), "Orders", user_id)


def format_order_text(order):
    """Форматирует заказ в читаемый вид."""
    drinks_text = "\n".join(
        [f"{drink['type']} ({drink.get('subtype', '')}), сахар: {drink.get('sugar', 'без сахара')}" for drink in
         order["drinks"]])
    return (
        f"Время заказа: {order['time']}\n"
        f"Место доставки: {order['location']}\n"
        f"Напитки:\n{drinks_text}\n"
        f"Статус: {order['status']}"
    )