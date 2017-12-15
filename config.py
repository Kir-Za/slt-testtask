import os
import logging

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
