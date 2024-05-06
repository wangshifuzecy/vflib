from datetime import datetime

import jwt
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from common.common_response import CommonResponse
from common.jwt_api import jwt_id
from models.book_model import BookModel
from models.user_model import UserModel
from resources import api,app
from services.user_service import UserService
import json
from common.constants import LOGIN_SECRET


@api.resource('/users/<int:user_id>')
class UserResource(Resource):
    def get(self, user_id: int):
        user_model = UserService().get_user_by_id(user_id)

        if user_model:
            return CommonResponse.success_response(user_model.serialize())
        else:
            return CommonResponse.error_response(f"未找到id为{user_id}的用户")

    def put(self, user_id: int):
        request_json = request.json
        if request_json:
            # 解构字典 但是没有参数校验
            user_model = UserModel(**request_json)
            UserService().update_user(user_id, user_model)
            return CommonResponse.success_response(user_model.serialize())
        else:
            return CommonResponse.error_response("用户信息更新失败")


    @jwt_id(['admin'])
    def delete(self, user_id: int):
        try:
            UserService().remove_user(user_id)
        except SQLAlchemyError as e:
            return CommonResponse.error_response("删除失败, 请检查用户是否有借阅记录")
        return CommonResponse.success_no_data()


@api.resource('/users')
class UserListResource(Resource):
    def get(self):
        user_list = UserService().get_all_users()
        # print(len(user_list))
        return CommonResponse.success_response([user_model.serialize() for user_model in user_list])

    def post(self):
        request_json = request.json
        if request_json:
            user_model = UserModel(**request_json)
            UserService().create_user(user_model)
            return CommonResponse.success_response(user_model.serialize())
        else:
            return CommonResponse.error_response("创建失败")


@api.resource('/users/login')
class UserLoginResource(Resource):
    def post(self):
        request_json = request.json
        if request_json:
            id = request_json.get('id')
            pwd = request_json.get('pwd')
            user_model = UserService().login_user(id, pwd)
            if user_model:
                jwt_token = jwt.encode({"id": id, "role": user_model.position}, LOGIN_SECRET, algorithm='HS256')
                return CommonResponse.success_response(jwt_token)
            else:
                return CommonResponse.error_response('卡号或密码错误')
        else:
            return CommonResponse.error_response("数据不是有效json")


