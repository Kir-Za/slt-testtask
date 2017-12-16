import logging
from datetime import datetime
from app.database import get_session
from app.models import Server, Rack
from app.utils import check_ip, check_free_slots, activate_server
from config import MAIN_OWNER, ENABLED_VOLUME, SELECTEL_ADDR, SEVER_STANDART_CORE, SEVER_STATUS_LIST,\
    START_SERVER_STATUS, ENABLED_INFO_CLASSES


module_logger = logging.getLogger('main_log')


def create_rack(owner, volume):
    """
    Создание пустой серверной стойки
    :param owner: Владелец (selectel или иной собственник)
    :param volume: Тип стойки - на 10 или 20
    :return: результат сосздания
    """
    tmp_session = get_session()
    try:
        owner = MAIN_OWNER if owner.lower() == MAIN_OWNER else 'other owner'
        if tmp_session is None:
            raise OSError
        new_rack = Rack(
            date_creation=datetime.now(),
            date_last_changes=datetime.now(),
            owner=owner,
            address=SELECTEL_ADDR,
            volume=ENABLED_VOLUME.get(volume, 10)
        )
        tmp_session.add(new_rack)
        tmp_session.commit()
        module_logger.info('Новая серверная стойка успешно создана.')
    except OSError:
        module_logger.error('Ошибка в назначении прав доступа к файловой директории.')
    except Exception as err:
        module_logger.error("Ошибка операции создания новой серверной стойки. %s" % str(err))
    finally:
        tmp_session.close()


def get_common_info(model_class, sort_by_date=False):
    """
    Получить краткую информацию по наличествующим стойкам.
    :return: Список стоек/серверов.
    """
    tmp_session = get_session()
    try:
        if model_class not in ENABLED_INFO_CLASSES:
            raise Exception("Неверно указана модель.")
        if sort_by_date:
            info_list = tmp_session.query(eval(model_class)).order_by('date_last_changes').all()
        else:
            info_list = tmp_session.query(eval(model_class)).order_by('id').all()
        return info_list
    except Exception as err:
        module_logger.error("Ошибка запроса общей информации. %s" % str(err))
    finally:
        tmp_session.close()


def get_detail_rack_info(id):
    """
    Получение детальной информации по конкретной стойке
    """
    tmp_session = get_session()
    try:
        one_rack = tmp_session.query(Rack).get(int(id))
        return {
            'id': one_rack.id,
            'date_creation': one_rack.date_creation,
            'date_last_changes': one_rack.date_last_changes,
            'owner': one_rack.owner,
            'address': one_rack.address,
            'volume': one_rack.volume,
            'servers_id': [x.id for x in one_rack.servers]
        }
    except Exception as err:
        module_logger.error('Ошибка запроса списка серверов. %s' % str(err))
    finally:
        tmp_session.close()


def get_detail_server_info(id):
    """
    Получение детальной информации по серверу
    """
    tmp_session = get_session()
    try:
        one_server = tmp_session.query(Server).get(int(id))
        return {
            'id': one_server.id,
            'date_creation': one_server.date_creation,
            'date_last_changes': one_server.date_last_changes,
            'server_ip': one_server.server_ip,
            'server_ram': one_server.server_ram,
            'server_core': one_server.server_core,
            'optical_port': one_server.optical_port,
            'operator': one_server.operator,
            'status': get_server_status(id),
            'pay_time': one_server.pay_time.timestamp() if one_server.pay_time else None,
            'rack_id': one_server.rack_id
        }
    except Exception as err:
        module_logger.error('Ошибка запроса списка серверов. %s' % str(err))
    finally:
        tmp_session.close()


def remove_rack(id):
    """
    Удаление пустой стойки.
    :param id: идентификатор стойки
    :return: id удаленного срвера
    """
    tmp_session = get_session()
    try:
        del_rack = tmp_session.query(Rack).get(int(id))
        if len(del_rack.servers):
            module_logger.error('Удаление стойки с функционирующими серверамии невозможно')
            return False
        else:
            tmp_session.delete(del_rack)
            tmp_session.commit()
            module_logger.info('Пустая серверная стойка с id = {0} удалена.'.format(str(id)))
            return id
    except Exception as err:
        module_logger.error('Ошибка при удалении серверной стойки. %s' % str(err))
    finally:
        tmp_session.close()


def create_and_add_server(rack_id, server_ip, ram):
    """
    Создание нового сервера и добавление его в серверную стойку.
    :param rack_id: id стойки
    :param server_ip: назначенный ip
    :param ram: объем оперативной памяти
    :return: id созданного сервера
    """
    tmp_session = get_session()
    try:
        rack = tmp_session.query(Rack).get(int(rack_id))
        check_free_slots(rack)
        new_server = Server(
            date_creation=datetime.now(),
            date_last_changes=datetime.now(),
            server_ip=check_ip(server_ip),
            server_ram=ram,
            server_core=SEVER_STANDART_CORE,
            optical_port=False,
            status=SEVER_STATUS_LIST[START_SERVER_STATUS]
        )
        tmp_session.add(new_server)
        tmp_session.commit()
        module_logger.info('Создан новый сервер с id=%s' % str(new_server.id))
        add_server_to_rack(new_server.id, rack.id, new=True)
        return new_server.id
    except AttributeError:
        module_logger.error('Ошибка указания ip создаваемого сервера.')
        return False
    except Exception as err:
        module_logger.error(err)
        return False
    finally:
        tmp_session.close()


def add_server_to_rack(server_id, rack_id, new=False):
    """
    Добавление сервера в стойку
    :param server_id: сервер
    :param rack_id: созданная ранее стойка
    :param new: добавляется новый или перемещаем существующий
    :return:
    """
    tmp_session = get_session()
    try:
        rack = tmp_session.query(Rack).get(int(rack_id))
        if not new:
            check_free_slots(rack)
        server = tmp_session.query(Server).get(int(server_id))
        rack.servers.append(server)
        tmp_session.commit()
        module_logger.info('В серверную стойку с id={0} добавлен сервер с id={1}'.format(str(rack_id), str(server_id)))
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def remove_server(id):
    """
    Удаление сервера.
    :param id: целевой id
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status != SEVER_STATUS_LIST[-1]:
            raise Exception("Для удаления необходимо сервер {0} перевести в состяние {1}".format(str(id),
                                                                                                 SEVER_STATUS_LIST[-1]))
        tmp_session.delete(server)
        tmp_session.commit()
        module_logger.info('Удален сервер с id=%s' % str(id))
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def sell_server(id, new_operator):
    """
    Продать сервер
    :param id: целевой id
    :param new_operator: новый пользователь
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status != SEVER_STATUS_LIST[-1]:
            raise Exception("Нельзя продать сервер находящийся в состоянии %s" % SEVER_STATUS_LIST[-1])
        server.operator = new_operator
        tmp_session.commit()
        module_logger.info('Сервер продан. Новый оператор - %s' % str(new_operator))
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def on_optical_port(id):
    """
    Продать сервер
    :param id: целевой id
    :param new_operator: новый пользователь
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status != SEVER_STATUS_LIST[-1]:
            raise Exception("Нельзя подключить оптический порт к серверу в состоянии %s" % SEVER_STATUS_LIST[-1])
        server.optical_port = True
        tmp_session.commit()
        module_logger.info('Сервер %s оснащен оптическим каналом связи' % str(id))
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def move_to_del(id):
    """
    Перевести сервер в состояние Deleted
    :param id: целевой сервер
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status == SEVER_STATUS_LIST[-1]:
            raise Exception("Сервер уже в состоянии %s" % SEVER_STATUS_LIST[-1])
        server.status = SEVER_STATUS_LIST[-1]
        tmp_session.commit()
        module_logger.info('Сервер {0} переведен в состояние {1}'.format(str(id), SEVER_STATUS_LIST[-1]))
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def get_server_status(id):
    """
    Запрос состояния
    :param id: целевой сервер
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status == SEVER_STATUS_LIST[1]:
            activate_server(tmp_session, server)
        return server.status
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()


def to_pay(id):
    """
    Оплатить сервер
    :param id: целевой id
    """
    tmp_session = get_session()
    try:
        server = tmp_session.query(Server).get(int(id))
        if server.status != SEVER_STATUS_LIST[0]:
            raise Exception("Невозможно оплатить сервер, находящийся в состоянии отличном от %s" % SEVER_STATUS_LIST[0])
        server.status = SEVER_STATUS_LIST[1]
        tmp_session.commit()
        server.pay_time = datetime.today()
        tmp_session.commit()
        return server.status
    except Exception as err:
        module_logger.error(err)
    finally:
        tmp_session.close()
