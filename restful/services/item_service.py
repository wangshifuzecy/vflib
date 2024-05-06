from sqlalchemy import Select, and_
from models.item_model import ItemModel
from models.record_model import RecordModel
from resources import db


class ItemService:
    def get_all_items(self):
        query = Select(ItemModel).order_by(ItemModel.id)
        return db.session.scalars(query).all()

    def get_item_by_id(self, item_id):
        return db.session.get(ItemModel, item_id)

    def get_by_book_id(self, book_id: int):
        query = Select(ItemModel).filter_by(book_id=book_id).order_by(ItemModel.id)
        return db.session.scalars(query).all()

    def get_not_borrow(self, book_id: int):
        query = Select(ItemModel).where(and_(ItemModel.book_id == book_id, ItemModel.is_borrowed == False))
        return db.session.scalars(query).all()

    def borrow(self, record_model: RecordModel):
        existing_item = self.get_item_by_id(record_model.item_id)
        if existing_item:
            existing_item.record_id = record_model.id
            existing_item.is_borrowed = True
            db.session.commit()
        else:
            raise Exception(f'码号定位为{record_model.item_id}的书不存在')

    def return_item(self, item_id: int):
        existing_item = self.get_item_by_id(item_id)
        if existing_item:
            existing_item.is_borrowed = False
            existing_item.record_id = None
            db.session.commit()
        else:
            raise Exception(f'码号定位为{item_id}的书不存在')

