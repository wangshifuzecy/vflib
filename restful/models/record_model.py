from sqlalchemy import Integer, String, TIMESTAMP, Float, ForeignKey, Boolean, Column, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from resources import db


class RecordModel(db.Model):
    __tablename__ = 'borrow_records'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str] = mapped_column(String(255))
    book_name: Mapped[str] = mapped_column(String(255))
    borrow_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)
    return_time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)

    def serialize(self):
        borrow_time_iso = self.borrow_time.strftime('%Y-%m-%d %H:%M:%S') if self.borrow_time else None
        return_time_iso = self.return_time.strftime('%Y-%m-%d %H:%M:%S') if self.return_time else None

        return {
            'id': self.id,
            'book_id': self.book_id,
            'item_id': self.item_id,
            'user_id': self.user_id,
            'isbn': self.isbn,
            'book_name': self.book_name,
            'borrow_time': borrow_time_iso,
            'return_time': return_time_iso
        }
