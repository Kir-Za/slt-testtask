import re
import logging
import random
from time import sleep
from app.database import get_session
from app.models import Server
from config import SEVER_STATUS_LIST, PREPARE_TIME_RANGE

module_logger = logging.getLogger('main_log')

def check_ip(new_ip):
    """
    Проверка доступности ip
    :param new_ip: проверяемый ip в случае его корректности
    :return: корректный ip
    """
    ture_format = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", new_ip)
    if ture_format:
        tmp_session = get_session()
        server_list = [server.server_ip for server in tmp_session.query(Server).all()]
        tmp_session.close()
        if ture_format.group() not in server_list:
            return ture_format.group()
    raise AttributeError


def check_free_slots(rack):
    """
    Проверка наличия свободных слотов
    :param rack: серверная стойка
    """
    if len(rack.servers) == rack.volume:
        raise Exception('Ошибка создания и добавления сервера. Серверная стойка не имеет свободных слотов.')
    elif len(rack.servers) > rack.volume:
        raise Exception('Ошибка манипуляции с параметрами серверной стойки. Превышено максимально допустимый объем')


def activate_server(tmp_session, server):
    """
    Перевод оплаченного сервера в активное состояние
    :param tmp_session: сессия запроса
    :param server: целевой сервер
    """
    module_logger.info('Выполняется перевод оплаченного сервера в рабочее состояние.'
                       ' Эта операция может занять некоторе время.')
    sleep(random.randint(PREPARE_TIME_RANGE[0], PREPARE_TIME_RANGE[1]))
    server.status = SEVER_STATUS_LIST[2]
    tmp_session.commit()
    module_logger.info('Сервер {0} переведен в состояние {1}'.format(str(server.id), SEVER_STATUS_LIST[2]))
