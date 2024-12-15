from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)  # Поле для ФИО
    email = Column(String, unique=True, index=True)  # Поле для email
    address = Column(String)  # Поле для адреса
    study_group = Column(String)  # Поле для учебной группы
    passport = Column(String)  # Поле для паспорта
    room_type = Column(String)  # Поле для типа комнаты
    building = Column(String)  # Поле для корпуса
    password = Column(String)  # Поле для пароля

