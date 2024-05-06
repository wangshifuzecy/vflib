from werkzeug.exceptions import HTTPException

from flask import jsonify
from werkzeug.exceptions import HTTPException
from common.common_response import CommonResponse


def http_handle_exception(e):
    return CommonResponse.error_response("URL not found", 20)
