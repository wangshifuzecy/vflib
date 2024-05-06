from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from common.common_response import CommonResponse
from models.record_model import RecordModel
from resources import api
from services.record_service import RecordService


@api.resource('/records')
class RecordListResource(Resource):
    def get(self):
        record_list = RecordService().get_all_records()
        return CommonResponse.success_response([record_model.serialize() for record_model in record_list])

    def post(self):
        request_json = request.json
        if request_json:
            record_model = RecordModel(**request_json)
            record_model = RecordService().add_record(record_model)
            return CommonResponse.success_response(record_model.serialize())
        else:
            return CommonResponse.error_response(f'json格式不正确')


@api.resource('/records/book_id/<int:book_id>')
class RecordByBookIdResource(Resource):
    def get(self, book_id: int):
        record_list = RecordService().get_record_by_book(book_id)
        return CommonResponse.success_response([record_model.serialize() for record_model in record_list])


@api.resource('/records/user_id/<int:user_id>')
class RecordByUserIdResource(Resource):
    def get(self, user_id: int):
        record_list = RecordService().get_record_by_user(user_id)
        return CommonResponse.success_response([record_model.serialize() for record_model in record_list])


@api.resource('/records/item_id/<int:item_id>')
class RecordByItemIdResource(Resource):
    def get(self, item_id: int):
        record_model = RecordService().get_record_by_item(item_id)
        return CommonResponse.success_response(record_model.serialize())


@api.resource('/records/id/<int:record_id>')
class RecordByIdResource(Resource):
    def get(self, record_id: int):
        record_model = RecordService().get_record_by_id(record_id)
        return CommonResponse.success_response(record_model.serialize())

    def delete(self, record_id: int):
        RecordService().remove_record_by_id(record_id)
        record_list = RecordService().get_all_records()
        return CommonResponse.success_response([record_model.serialize() for record_model in record_list])

    def put(self, record_id: int):
        request_json = request.json
        if request_json:
            record_model = RecordModel(**request_json)
            result = RecordService().update_record_by_id(record_model, record_id)
            return CommonResponse.success_response(result.serialize())
        else:
            return CommonResponse.error_response(f'json格式不正确')
