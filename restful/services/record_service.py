from sqlalchemy import Select, and_
from models.record_model import RecordModel
from resources import db


class RecordService:
    def get_all_records(self):
        query = Select(RecordModel).order_by(RecordModel.id)
        return db.session.scalars(query).all()

    def get_record_by_id(self, record_id: int):
        return db.session.get(RecordModel, record_id)

    def get_record(self, record_model: RecordModel):
        query = Select(RecordModel).where(and_(RecordModel.item_id == record_model.item_id, RecordModel.borrow_time == record_model.borrow_time))
        return db.session.scalars(query).all()[0]

    def get_record_by_book(self, book_id: int):
        query = Select(RecordModel).filter_by(book_id=book_id).order_by(RecordModel.id)
        return db.session.scalars(query).all()

    def get_record_by_user(self, user_id: int):
        query = Select(RecordModel).filter_by(user_id=user_id).order_by(RecordModel.id)
        return db.session.scalars(query).all()

    def get_record_by_item(self, item_id: int):
        query = Select(RecordModel).filter_by(item_id=item_id).order_by(RecordModel.id)
        return db.session.scalars(query).all()

    def remove_record_by_id(self, record_id: int):
        existing_record = self.get_record_by_id(record_id)
        if existing_record:
            db.session.delete(existing_record)
            db.session.commit()
        else:
            raise Exception(f'id 为{record_id}的记录不存在')

    def add_record(self, record_model: RecordModel):
        db.session.add(record_model)
        db.session.commit()
        return self.get_record(record_model)

    def update_record_by_id(self, record_model: RecordModel, record_id: int):
        existing_record = self.get_record_by_id(record_id)
        if existing_record:
            existing_record = record_model
            db.session.commit()
        else:
            raise Exception(f'id 为{record_id}的记录不存在')
