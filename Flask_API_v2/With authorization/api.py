from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from store import store
from users import username_table, userid_table


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


def abort_if_item_doesnt_exist(name):
    if not list(filter(lambda x: x['name'] == name, store)):
        abort(404, message="Item '{}' doesn't exist".format(name))


def abort_if_item_exists(name):
    if list(filter(lambda x: x['name'] == name, store)):
        abort(404, message="Item '{}' have already exist".format(name))


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @staticmethod
    @jwt_required()
    def get(name):
        abort_if_item_doesnt_exist(name)
        return list(filter(lambda x: x['name'] == name, store))[0]

    @staticmethod
    @jwt_required()
    def post(name):
        abort_if_item_exists(name)
        new_item = {'name': name,
                    'price': Item.parser.parse_args()['price']}
        store.append(new_item)
        return new_item, 201

    @staticmethod
    @jwt_required()
    def put(name):
        item = list(filter(lambda x: x['name'] == name, store))
        if item:
            item[0]['price'] = Item.parser.parse_args()['price']
            return item[0], 201
        new_item = {'name': name,
                    'price': Item.parser.parse_args()['price']}
        store.append(new_item)
        return new_item, 201

    @staticmethod
    @jwt_required()
    def delete(name):
        abort_if_item_doesnt_exist(name)
        store.remove(list(filter(lambda x: x['name'] == name, store))[0])
        return '', 204


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, action='append')

    @staticmethod
    @jwt_required()
    def get():
        return {'items': store}

    @staticmethod
    @jwt_required()
    def post():
        new_items = []
        for item in ItemList.parser.parse_args()['items']:
            abort_if_item_exists(item['name'])
        for item in ItemList.parser.parse_args()['items']:
            store.append(item)
            new_items.append(item)
        return {'new_items': new_items}, 201


@app.route('/protected', methods=["GET"])
@jwt_required()
def protected():
    return f'{current_identity}'


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(debug=True)
