from sqlalchemy import Integer, String, TIMESTAMP, Float, ForeignKey, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column

from resources import db



class ItemModel(db.Model):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), nullable=False)
    is_borrowed: Mapped[bool] = mapped_column(Boolean, default=False)
    record_id: Mapped[int] = mapped_column(Integer, ForeignKey('borrow_records.id'))

    def serialize(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'is_borrowed': self.is_borrowed,
            'record_id': self.record_id
        }
