from datetime import datetime
from for_db_tasks import insert_into_db_data, get_data_from_column, get_all_users


def create_order(user_id, drinks, location):
    """
    Создает новый заказ и сохраняет его в базу данных.
    :param user_id: ID пользователя
    :param drinks: Список напитков
    :param location: Место доставки
    :return: Словарь с заказом
    """
    order = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "оформлен",
        "drinks": drinks,
        "location": location,
        "user_id": user_id
    }
    save_order_to_db(user_id, order)
    return order


def save_order_to_db(user_id, order):
    """
    Сохраняет заказ в базу данных.
    :param user_id: ID пользователя
    :param order: Словарь с заказом
    """
    current_orders = get_data_from_column("Orders", user_id)
    if not current_orders:
        current_orders = []
    else:
        current_orders = eval(current_orders)

    current_orders.append(order)
    insert_into_db_data(str(current_orders), "Orders", user_id)


def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: Список заказов
    """
    all_orders = []
    users = get_all_users()
    for user in users:
        user_orders = get_data_from_column("Orders", user["id"])
        if user_orders:
            user_orders = eval(user_orders)
            all_orders.extend(user_orders)
    return all_orders


def format_order_text(order):
    """
    Форматирует заказ в читаемый вид.
    :param order: Словарь с заказом
    :return: Текст заказа
    """
    drinks_text = "\n".join(
        [f"{drink['type']} ({drink.get('subtype', '')}), сахар: {drink.get('sugar', 'без сахара')}" for drink in
         order["drinks"]])
    return (
        f"Время заказа: {order['time']}\n"
        f"Место доставки: {order['location']}\n"
        f"Напитки:\n{drinks_text}\n"
        f"Статус: {order['status']}"
    )


def change_order_status(order_index, new_status):
    """
    Изменяет статус заказа и удаляет его, если статус "выдан".
    :param order_index: Индекс заказа в списке
    :param new_status: Новый статус заказа
    :return: Обновленный список заказов
    """
    all_orders = get_all_orders()
    if order_index < 0 or order_index >= len(all_orders):
        raise IndexError("Неверный индекс заказа.")

    order = all_orders[order_index]
    order["status"] = new_status

    # Если статус "выдан", удаляем заказ
    if new_status == "выдан":
        user_id = order["user_id"]
        user_orders = eval(get_data_from_column("Orders", user_id))
        user_orders = [o for o in user_orders if o != order]
        insert_into_db_data(str(user_orders), "Orders", user_id)
    else:
        save_order_to_db(order["user_id"], order)

    return all_orders


def notify_admins(bot, order):
    """
    Уведомляет админов о новом заказе.
    :param bot: Объект бота
    :param order: Словарь с заказом
    """
    admin_list = ladmins()
    order_text = format_order_text(order)
    for admin_id in admin_list:
        bot.send_message(admin_id, f"Новый заказ:\n{order_text}")


def notify_user(bot, user_id, message):
    """
    Уведомляет пользователя об изменении статуса заказа.
    :param bot: Объект бота
    :param user_id: ID пользователя
    :param message: Текст уведомления
    """
    bot.send_message(user_id, message)