import os
import logging

# Константы
MAIN_OWNER = 'selectel'
SELECTEL_ADDR = '196084, RussinFederation, SPb'
ENABLED_VOLUME = {'20': 20, '10': 10}
SEVER_STANDART_CORE = 'Intel Xeon E3-1230 3.4x4'
SEVER_STATUS_LIST = ['Unpaid', 'Paid', 'Active', 'Deleted']
START_SERVER_STATUS = 0
ENABLED_INFO_CLASSES = ['Rack', 'Server']
PREPARE_TIME_RANGE = [5, 15]


# Конфигурация БД
DATABASE_NAME = 'hardware.db'

# Конфигурация логгера
logger = logging.getLogger('main_log')
logger.setLevel(logging.INFO)
templ = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
term = logging.StreamHandler()
term.setFormatter(templ)
logger.addHandler(term)



#class Config(object):
#    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
