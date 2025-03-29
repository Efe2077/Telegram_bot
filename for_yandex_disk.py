import os
from dotenv import load_dotenv
import yadisk

load_dotenv()
WHOLE_CLUBS = []
T = os.getenv('YD')
Y = yadisk.YaDisk(token=T)

# Заполняем список существующих клубов при запуске
for el in Y.listdir('/Music'):
    WHOLE_CLUBS.append(el['name'])


def download_file_to_club(club, file_name, file_data, apparatus=None):
    """
    Загружает файл напрямую на Яндекс.Диск
    :param club: Название клуба (папки)
    :param file_name: Имя файла (без расширения)
    :param file_data: Бинарные данные файла
    :param apparatus: Вид снаряда (добавляется к имени файла)
    :return: True если успешно, False если ошибка
    """
    try:
        if club not in WHOLE_CLUBS:
            return False  # Клуба не существует

        # Формируем окончательное имя файла
        if apparatus:
            base_name, ext = os.path.splitext(file_name)
            final_name = f"{base_name}_{apparatus}{ext}"
        else:
            final_name = file_name

        # Загружаем файл
        from io import BytesIO
        file_stream = BytesIO(file_data)
        file_stream.name = final_name

        try:
            Y.upload(file_stream, f'/Music/{club}/{final_name}')
            return True
        except yadisk.exceptions.PathExistsError:
            return False  # Файл уже существует
        except Exception as e:
            print(f'Ошибка загрузки на Яндекс.Диск: {e}')
            return False

    except Exception as e:
        print(f'Ошибка в download_file_to_club: {e}')
        return False