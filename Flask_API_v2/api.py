from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

store = [
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


def abort_if_item_doesnt_exist(name):
    if not list(filter(lambda x: x['name'] == name, store)):
        abort(404, message="Item '{}' doesn't exist".format(name))


def abort_if_item_exists(name):
    if list(filter(lambda x: x['name'] == name, store)):
        abort(404, message="Item '{}' have already exist".format(name))


class Item(Resource):
    parser.add_argument('price')

    def get(self, name):
        abort_if_item_doesnt_exist(name)
        return list(filter(lambda x: x['name'] == name, store))[0]

    def post(self, name):
        abort_if_item_exists(name)
        new_item = {'name': name,
                    'price': parser.parse_args()['price']}
        store.append(new_item)
        return new_item, 201

    def put(self, name):
        item = list(filter(lambda x: x['name'] == name, store))
        if item:
            item[0]['price'] = parser.parse_args()['price']
            return item[0], 201
        new_item = {'name': name,
                    'price': parser.parse_args()['price']}
        store.append(new_item)
        return new_item, 201

    def delete(self, name):
        if list(filter(lambda x: x['name'] == name, store)):
            abort(404, message="Item '{}' have already exist".format(name))
        store.remove(list(filter(lambda x: x['name'] == name, store))[0])
        return '', 204


class ItemList(Resource):
    parser.add_argument('items', type=dict, action='append')

    def get(self):
        return {'items': store}

    def post(self):
        new_items = []
        for item in parser.parse_args()['items']:
            abort_if_item_exists(item['name'])
        for item in parser.parse_args()['items']:
            store.append(item)
            new_items.append(item)
        return {'new_items': new_items}, 201


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
