from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, abort

from models.items import ItemModel, db


def does_item_exist(name):
    print(ItemModel.find_by_name(name))
    if ItemModel.find_by_name(name) is not None:
        return True
    return False


def abort_if_item_doesnt_exist(name):
    if not does_item_exist(name):
        return abort(404, message="item '{}' doesn't exist".format(name))


def abort_if_item_exist(name):
    if does_item_exist(name):
        abort(404, message="item '{}' has already exist".format(name))


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @staticmethod
    @jwt_required()
    def get(name):
        abort_if_item_doesnt_exist(name)
        item = ItemModel.find_by_name(name)
        return {'item': item.json()}, 201

    @staticmethod
    @jwt_required()
    def post(name):
        abort_if_item_exist(name)
        price = Item.parser.parse_args()['price']
        try:
            price = int(price)
            new_item = {'name': name,
                        'price': price}
            new_item = ItemModel(**new_item)
            new_item.add_item()
            return {'new_item': new_item.json()}, 201
        except:
            abort(404, message='price parameter must be integer')

    @staticmethod
    @jwt_required()
    def put(name):
        price = Item.parser.parse_args()['price']
        try:
            price = int(price)
            if does_item_exist(name):
                changed_item = ItemModel.find_by_name(name)
                changed_item.price = price
                db.session.commit()
                return {'changed_item': changed_item.json()}, 201
            new_item = {'name': name,
                        'price': price}
            new_item = ItemModel(**new_item)
            new_item.add_item()
            return {'new_item': new_item.json()}, 201
        except:
            abort(404, message='price parameter must be integer')

    @staticmethod
    @jwt_required()
    def delete(name):
        abort_if_item_doesnt_exist(name)
        deleted_item = Item.parser.parse_args()
        deleted_item = ItemModel.find_by_name(name)
        deleted_item.delete_item()
        return {'message': 'item {} was deleted'.format(name)}, 201


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, action='append')

    @staticmethod
    @jwt_required()
    def get():
        items = [i.json() for i in ItemModel.query.all()]
        if items:
            return {'items': items}, 201
        return abort(404, message="items don't exist")

    @staticmethod
    @jwt_required()
    def post():
        new_items = []
        items = ItemList.parser.parse_args()['items']
        if items:
            for item in items:
                abort_if_item_exist(item['name'])
                try:
                    price = int(item['price'])
                except:
                    return abort(404, message='price parameter must be integer')
            for item in items:
                new_item = {'name': item['name'],
                            'price': item['price']}
                new_item = ItemModel(**new_item)
                new_item.add_item()
                new_items.append(new_item.json())
            return {'new_items': new_items}, 201
        return {"message": "items list mustn't be empty"}, 404

    @staticmethod
    @jwt_required()
    def delete():
        items = ItemList.parser.parse_args()['items']
        if items:
            for item in items:
                abort_if_item_doesnt_exist()(item['name'])
            for item in items:
                Item.delete(item['name'])
            return {'message': 'items was deleted'}, 201
        return {"message": "items list mustn't be empty"}, 404
