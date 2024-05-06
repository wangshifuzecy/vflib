from flask import request
from flask_restful import Resource

from common.common_response import CommonResponse
from models.record_model import RecordModel
from resources import api
from services.item_service import ItemService
from services.record_service import RecordService


@api.resource('/items')
class ItemListResource(Resource):
    def get(self):
        item_list = ItemService().get_all_items()
        return CommonResponse.success_response([item_model.serialize() for item_model in item_list])


@api.resource('/items/id/<int:item_id>')
class ItemResource(Resource):
    def get(self, item_id: int):
        item_model = ItemService().get_item_by_id(item_id)
        return CommonResponse.success_response(item_model.serialize())


@api.resource('/items/book_id/<int:book_id>')
class ItemByBookIdResource(Resource):
    def get(self, book_id: int):
        item_list = ItemService().get_by_book_id(book_id)
        if len(item_list) == 0:
            return CommonResponse.error_response(f"没有图书id为{book_id}的书")
        return CommonResponse.success_response([item_model.serialize() for item_model in item_list])


# 查找可已借出的图书
@api.resource('/items/not_borrow/book_id/<int:book_id>')
class ItemNotBorrowByBookId(Resource):
    def get(self, book_id: int):
        item_list = ItemService().get_not_borrow(book_id)
        if len(item_list) == 0:
            return CommonResponse.error_response(f"没有图书id为{book_id}的可借图书")
        return CommonResponse.success_response([item_model.serialize() for item_model in item_list])


@api.resource('/items/borrow')
class ItemBorrowResource(Resource):
    def post(self):
        request_json = request.json
        if request_json:
            record_model = RecordModel(**request_json)
            ItemService().borrow(record_model)
            item_model = ItemService().get_item_by_id(record_model.item_id)
            return CommonResponse.success_response(item_model.serialize())
        else:
            return CommonResponse.error_response(f'json格式不正确')


@api.resource('/items/return/id/<int:item_id>')
class ItemReturnResource(Resource):
    def post(self, item_id: int):
        ItemService().return_item(item_id)
        item_model = ItemService().get_item_by_id(item_id)
        return CommonResponse.success_response(item_model.serialize())