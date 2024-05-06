from sqlalchemy import Select

from models.book_model import BookModel
from resources import db

class BookService:
    def get_book_by_id(self, book_id: int):
        return db.session.get(BookModel, book_id)

    def get_all_books(self):
        query = Select(BookModel).order_by(BookModel.id)
        return db.session.scalars(query).all()

    def create_book(self, book_model: BookModel):
        db.session.add(book_model)
        db.session.commit()
        return book_model

    def update_book(self, book_id: int, book_model: BookModel):
        existing_book = self.get_book_by_id(book_id)
        if existing_book:
            existing_book = book_model
            db.session.commit()
        else:
            raise Exception(f'id 为{book_id}的书不存在')

    def remove_book(self, book_id: int):
        existing_book = self.get_book_by_id(book_id)
        if existing_book:
            db.session.delete(existing_book)
            db.session.commit()
        else:
            raise Exception(f'id 为{book_id}的书不存在')

    # 隐藏或显现
    def hidden_book(self, book_id: int):
        existing_book = self.get_book_by_id(book_id)
        if existing_book:
            existing_book.is_hidden = not existing_book.is_hidden
            db.session.commit()
        else:
            raise Exception(f'id 为{book_id}的书不存在')
