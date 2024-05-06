from sqlalchemy import Select, or_

from models.user_model import UserModel
from resources import db


class UserService:
    def get_user_by_id(self, user_id: int):
        return db.session.get(UserModel, user_id)

    def update_user(self, user_id: int, user_model: UserModel):
        existing_user = self.get_user_by_id(user_id)
        if existing_user:
            existing_user = user_model
            db.session.commit()
        else:
            raise Exception(f'Book with id {user_id} does not exist')

    def create_user(self, user_model: UserModel):
        db.session.add(user_model)
        print(db.session.commit())
        return user_model

    def login_user(self, user_id: str, pwd: str):
        query = Select(UserModel).where(UserModel.id == user_id)
        user_model = db.session.scalars(query).first()
        if user_model and user_model.pwd == pwd:
            return user_model
        else:
            return None

    # get all students or teachers, no admin
    def get_all_users(self):
        query = Select(UserModel).where(or_(UserModel.position == 'student', UserModel.position == 'teacher'))
        return db.session.scalars(query).all()

    def remove_user(self, user_id: int):
        existing_user = self.get_user_by_id(user_id)
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        else:
            raise Exception(f'id 为{user_id}的书不存在')

