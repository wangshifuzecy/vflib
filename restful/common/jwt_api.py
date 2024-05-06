from functools import wraps
from flask import request
from common.common_response import CommonResponse
from common.constants import LOGIN_SECRET
import jwt


def jwt_id(roles=None):
    default_roles = ['admin', 'student', 'teacher']
    def check_token(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt_token = request.headers.get('Authorization')
            if not jwt_token:
                return CommonResponse.error_response('请先登录', 10)
            # print(jwt_token)
            try:
                id_and_role = jwt.decode(jwt_token, LOGIN_SECRET, algorithms='HS256')
                if not id_and_role:
                    return CommonResponse.error_response('登录已失效, 请重新登录', 10)
                else:
                    role = id_and_role['role']
                    allowed_roles = roles if roles is not None else default_roles
                    if role not in allowed_roles:
                        return CommonResponse.error_response('权限不足', 11)
            except Exception as e:
                return CommonResponse.error_response('登录已失效, 请重新登录', 10)

            result = f(*args, **kwargs)
            return result

        return wrapper

    return check_token
