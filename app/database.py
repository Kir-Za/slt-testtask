import os
import logging
from sqlalchemy import create_engine
from config import DATABASE_NAME
from sqlalchemy.orm import sessionmaker
from app.models import Base

module_logger = logging.getLogger('main_log')


def create_db_file():
    engine = create_engine(''.join(['sqlite:///', DATABASE_NAME]))
    Base.metadata.create_all(engine)
    module_logger.info("Создан пустой объект базы данных")


def create_session():
    engine = create_engine(''.join(['sqlite:///', DATABASE_NAME]))
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    module_logger.info("Сессия работы с базой данных создана")
    return Session()


def get_session():
    if DATABASE_NAME not in os.listdir('.'):
        module_logger.info("База данных на диске не обнаружена.")
        create_db_file()
    return create_session()
