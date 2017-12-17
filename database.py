import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_NAME
from models import Base

module_logger = logging.getLogger('main_log')


def create_db_file():
    """
    Создали файл БД в текущей директории
    """
    try:
        engine = create_engine(''.join(['sqlite:///', DATABASE_NAME]))
        Base.metadata.create_all(engine)
        module_logger.info("Создан пустой объект базы данных")
    except Exception as err:
        module_logger.error("Ошибка при создании файла БД. %s" % str(err))


def create_session():
    """
    Получили сессию с существующей БД
    :return: объект сессии
    """
    try:
        engine = create_engine(''.join(['sqlite:///', DATABASE_NAME]))
        Base.metadata.bind = engine
        Session = sessionmaker(bind=engine)
        module_logger.info("Сессия работы с базой данных создана")
        return Session()
    except Exception as err:
        module_logger.error("Ошибка создания сессии. %s" % str(err))
        return None


def get_session():
    """
    Проверили наличие БД и создали сессию по ней
    :return: объект сессии
    """
    if DATABASE_NAME not in os.listdir('.'):
        module_logger.info("База данных на диске не обнаружена.")
        create_db_file()
    return create_session()
