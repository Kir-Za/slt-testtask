from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    """
    Модель сервера.
    server_ram - объем оперативной памяти
    server_core - параметры процессора
    optical_port - наличие/отсутствие оптического порта
    status - статус (unpaid, paid, active, deleted)
    pay_time - оплаченное время
    """
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime)
    date_last_changes = Column(DateTime)
    server_ip = Column(String, nullable=False)
    server_ram = Column(Integer)
    server_core = Column(String, nullable=False)
    optical_port = Column(Boolean)
    operator = Column(String)
    status = Column(String, nullable=False)
    pay_time = Column(DateTime)
    rack_id = Column(Integer, ForeignKey('rack.id'))


    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'date_last_changes':
            self.date_last_changes = datetime.now()


class Rack(Base):
    """
    Модель серверной стойки.
    operator - текущий оператор
    owner - принадлежность
    address - место расположения
    volume - количество слотов (10 или 20)
    """
    __tablename__ = 'rack'
    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime)
    date_last_changes = Column(DateTime)
    owner = Column(String, nullable=False)
    address = Column(String, nullable=False)
    volume = Column(Integer)
    servers = relationship('Server', backref='server_rack')

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'date_last_changes':
            self.date_last_changes = datetime.now()
