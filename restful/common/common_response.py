from flask import jsonify

class CommonResponse:
    @staticmethod
    def success_response(data, msg="success"):
        if msg and msg != "success":
            if data:
                response = {
                    "status": 0,
                    "msg": msg,
                    "data": data
                }
            else:
                response = {
                    "status": 0,
                    "msg": msg,
                }
        else:
            if data:
                response = {
                    "status": 0,
                    "data": data
                }
            else:
                response = {
                    "status": 0,
                }
        return jsonify(response)

    @staticmethod
    def success_no_data():
        response = {
            "status": 0,
        }
        return jsonify(response)

    @staticmethod
    def error_response(msg="error", status=1):
        response = {
            "msg": msg,
            "status":  status
        }
        return jsonify(response)

    @staticmethod
    def error_data_response(data, msg="error", status=1):
        response = {
            "data": data,
            "msg": msg,
            "status":  status
        }
        return jsonify(response)

