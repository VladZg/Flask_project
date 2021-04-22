from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth import authenticate, identity
from items import Item, ItemList
from users import User, UserRegister

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=6656)
