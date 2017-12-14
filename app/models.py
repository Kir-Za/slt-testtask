from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime)
    date_last_changes = Column(DateTime)
    server_ip = Column(Integer)
    server_ram = Column(Integer)
    server_core = Column(String, nullable=False)
    optical_port = Column(Boolean)
    status = Column(String, nullable=False)
    pay_time = Column(TIMESTAMP)
    server_rack_id = Column(Integer, ForeignKey('rack.id'))
    server_rack = relationship("Rack", back_populates="children")

class Rack(Base):
    __tablename__ = 'rack'
    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime)
    date_last_changes = Column(DateTime)
    operator = Column(String)
    owner = Column(String, nullable=False)
    address = Column(String, nullable=False)
    volum = Column(Integer)
    servers = relationship("Server", back_populates="parent")


engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)