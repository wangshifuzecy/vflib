from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PythonEnum
from sqlalchemy.orm import Mapped, mapped_column
from resources import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[str] = mapped_column(String(255),nullable=False)
    username: Mapped[str] = mapped_column(String(255),nullable=False)
    position: Mapped[enumerate] = mapped_column(Enum('student', 'teacher', 'admin'), default='student')
    pwd: Mapped[str] = mapped_column(String(255))
    sex: Mapped[str] = mapped_column(String(255))
    addr: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    balance: Mapped[float] = mapped_column(Float(precision=2))

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'username': self.username,
            'position': self.position,
            'sex': self.sex,
            'addr': self.addr,
            'phone': self.phone,
            'balance': self.balance
        }