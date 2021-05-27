from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from flask_restful import Api
import os

from resources.users import UserRegister, RegisteredUsers
from resources.items import Item, ItemList
from db import db
from auth import authenticate, identity
from resources.stores import Store, StoreList


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
db.init_app(app)
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register/<string:username>')
api.add_resource(RegisteredUsers, '/users')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    if os.path.isfile('data.db'):
        os.remove('data.db')
    app.run(debug=True, port=6558)
