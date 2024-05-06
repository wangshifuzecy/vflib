from common.exception import  *
from resources import app

if __name__ == '__main__':
    app.register_error_handler(HTTPException, http_handle_exception)
    app.run(debug=True,port=5000)
