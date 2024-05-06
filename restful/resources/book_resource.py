from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from common.common_response import CommonResponse
from common.jwt_api import jwt_id
from models.book_model import BookModel
from resources import api
from services.book_service import BookService


@api.resource('/books/<int:book_id>')
class BookResource(Resource):
    def get(self, book_id: int):
        book_model = BookService().get_book_by_id(book_id)
        if book_model:
            return CommonResponse.success_response(book_model.serialize())
        else:
            return CommonResponse.error_response(f'未找到id为{book_id}的图书')

    @jwt_id(['admin'])
    def put(self, book_id: int):
        request_json = request.json
        if request_json:
            book_model = BookModel(**request_json)
            BookService().update_book(book_id, book_model)
            return CommonResponse.success_response(book_model.serialize())
        else:
            return CommonResponse.error_response(f'未找到id为{book_id}的图书')

    @jwt_id(['admin'])
    def delete(self, book_id: int):
        try:
            BookService().remove_book(book_id)
        except SQLAlchemyError as e:
            return CommonResponse.error_response("删除失败, 请检查图书是否有借阅记录")
        return CommonResponse.success_no_data()


@api.resource('/books')
class BookListResource(Resource):
    def get(self):
        book_list = BookService().get_all_books()
        return CommonResponse.success_response([book_model.serialize() for book_model in book_list])

    def post(self):
        request_json = request.json
        if request.json:
            book_model = BookModel(**request_json)
            BookService().create_book(book_model)
            return CommonResponse.success_response(book_model.serialize())
        else:
            return CommonResponse.error_response('上传格式错误', 30)


@api.resource('/books/<int:book_id>/hidden')
class BookHiddenResource(Resource):
    @jwt_id(['admin'])
    def post(self, book_id: int):
        BookService().hidden_book(book_id)
        book_model = BookService().get_book_by_id(book_id)
        return CommonResponse.success_response(book_model.serialize())
