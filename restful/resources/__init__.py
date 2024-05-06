from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import json
from common.exception import  *
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:1234@localhost/vflib'
db = SQLAlchemy(app)
api = Api(app)

from resources import user_resource
from resources import book_resource
from resources import record_resource
from resources import item_resource


