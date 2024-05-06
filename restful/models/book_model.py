from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from resources import db

class BookModel(db.Model):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float(precision=2))
    author: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))
    img: Mapped[str] = mapped_column(String(255))
    publisher: Mapped[str] = mapped_column(String(255))
    publish_time: Mapped[str] = mapped_column(String(255))
    info: Mapped[str] = mapped_column(String(255))
    pages: Mapped[int] = mapped_column(Integer)
    borrow_times: Mapped[int] = mapped_column(Integer, default=0)
    want: Mapped[int] = mapped_column(Integer, default=0)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'name': self.name,
            'price': self.price,
            'author': self.author,
            'category': self.category,
            'img': self.img,
            'publisher': self.publisher,
            'publish_time': self.publish_time,
            'info': self.info,
            'pages': self.pages,
            'borrow_times': self.borrow_times,
            'want': self.want,
            'is_hidden': self.is_hidden
        }