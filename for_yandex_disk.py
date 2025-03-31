import os
from dotenv import load_dotenv
import yadisk
import logging
from io import BytesIO

# Настройка логирования
logger = logging.getLogger(__name__)

load_dotenv()
WHOLE_CLUBS = []
T = os.getenv('YD')
Y = yadisk.YaDisk(token=T)

# Заполняем список клубов при запуске
try:
    WHOLE_CLUBS = [el['name'] for el in Y.listdir('/Music')]
    logger.info(f"Загружен список клубов: {len(WHOLE_CLUBS)}")
except Exception as e:
    logger.error(f"Ошибка загрузки клубов: {e}")


def download_file_to_club(club, file_name, file_data, apparatus=None):
    """Загружает файл на Яндекс.Диск с проверками"""
    try:
        if club not in WHOLE_CLUBS:
            logger.warning(f"Клуб не найден: {club}")
            return False, "Клуб не существует"

        # Нормализация имени файла
        base_name, ext = os.path.splitext(file_name)
        if apparatus:
            final_name = f"{base_name}_{apparatus}.mp3"
        else:
            final_name = f"{base_name}.mp3" if not ext else file_name

        # Проверка типа файла
        if not final_name.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
            return False, "Неподдерживаемый формат аудио"

        # Загрузка с прогрессом
        try:
            Y.upload(BytesIO(file_data), f'/Music/{club}/{final_name}')
            return True, "Файл успешно загружен"
        except yadisk.exceptions.PathExistsError:
            return False, "Файл уже существует"
        except Exception as e:
            logger.error(f"Ошибка загрузки: {e}")
            return False, f"Ошибка: {str(e)}"

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        return False, "Критическая ошибка при загрузке"