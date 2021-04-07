from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

STORE = [
    {
        'name': 'item1',
        'price': 1500
    },
    {
        'name': 'item2',
        'price': 2000
    },
    {
        'name': 'item3',
        'price': 777
    },
    {
        'name': 'item4',
        'price': 3699
    }
]


parser = reqparse.RequestParser()


def filter(name):
    if name not in list([item['name'] for item in STORE]):
        abort(404, message="Item '{}' doesn't exist".format(name))


class Item(Resource):

    parser.add_argument('price')

    def get(self, name):
        filter(name)
        return STORE[name]

    def post(self, name):
        if name in list([item['name'] for item in STORE]):
            abort(404, message="Item '{}' have already exist".format(name))
        new_item = {'name': name,
                    'price': parser.parse_args()['price']}
        STORE.append(new_item)
        return new_item, 201

    def put(self, name):
        for i in range(len(STORE)):
            if STORE[i]['name'] == name:
                STORE[i]['price'] = parser.parse_args()['price']
                return STORE[i], 201
        new_item = {'name': name,
                    'price': parser.parse_args()['price']}
        STORE.append(new_item)
        return new_item, 201

    def delete(self, name):
        filter(name)
        for i in range(len(STORE)):
            if STORE[i]['name'] == name:
                del STORE[i]
                return '', 204


class ItemList(Resource):
    parser.add_argument('name')
    parser.add_argument('price')

    def get(self):
        return STORE

    def post(self):
        pass
        return 201


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
