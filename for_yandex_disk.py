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


def init_clubs_list():
    """Инициализирует список клубов при запуске"""
    global WHOLE_CLUBS
    try:
        WHOLE_CLUBS = [el['name'] for el in Y.listdir('/Music')]
        logger.info(f"Загружен список клубов: {len(WHOLE_CLUBS)}")
        return True
    except Exception as e:
        logger.error(f"Ошибка загрузки клубов: {e}")
        return False


def upload_to_yadisk(club, file_name, file_data, progress_callback=None):
    """Загружает файл на Яндекс.Диск"""
    try:
        # Проверка существования клуба
        if club not in WHOLE_CLUBS:
            logger.warning(f"Клуб не найден: {club}")
            return False, "Клуб не существует"

        # Создаем путь для загрузки
        remote_path = f'/Music/{club}/{file_name}'

        # Загрузка с обработкой прогресса
        total_size = len(file_data)
        uploaded = 0
        chunk_size = 1024 * 1024  # 1MB chunks

        with BytesIO(file_data) as file_stream:
            while uploaded < total_size:
                chunk = file_stream.read(chunk_size)
                Y.upload(chunk, remote_path, overwrite=True)
                uploaded += len(chunk)
                if progress_callback:
                    progress_callback(uploaded, total_size)

        return True, "Файл успешно загружен"

    except yadisk.exceptions.PathExistsError:
        return False, "Файл уже существует"
    except yadisk.exceptions.YaDiskError as e:
        logger.error(f"Ошибка Яндекс.Диска: {e}")
        return False, f"Ошибка Яндекс.Диска: {str(e)}"
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        return False, "Критическая ошибка при загрузке"


# Инициализируем список клубов при импорте
init_clubs_list()