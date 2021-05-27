from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, abort

from models.stores import StoreModel, db
from models.items import ItemModel


def does_store_exist(name):
    if StoreModel.find_by_name(name) is not None:
        return True
    return False


def abort_if_store_doesnt_exist(name):
    if not does_store_exist(name):
        return abort(404, message="store '{}' doesn't exist".format(name))


def abort_if_store_exist(name):
    if does_store_exist(name):
        abort(404, message="store '{}' has already exist".format(name))


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_name')

    @staticmethod
    @jwt_required()
    def get(name):
        abort_if_store_doesnt_exist(name)
        store = StoreModel.find_by_name(name)
        return {'store': store.json()}, 201

    @staticmethod
    @jwt_required()
    def post(name):
        abort_if_store_exist(name)
        new_store = {'name': name}
        new_store = StoreModel(**new_store)
        new_store.add_store()
        return {'new_store': new_store.json()}, 201

    @staticmethod
    @jwt_required()
    def put(name):
        if does_store_exist(name):
            changed_store = StoreModel.find_by_name(name)
            new_name = Store.parser.parse_args()['new_name']
            abort_if_store_exist(new_name)
            changed_store.name = new_name
            db.session.commit()
            return {'changed_store': changed_store.json()}, 201
        new_store = {'name': name}
        new_store = StoreModel(**new_store)
        new_store.add_store()
        return {'new_store': new_store.json()}, 201

    @staticmethod
    @jwt_required()
    def delete(name):
        abort_if_store_doesnt_exist(name)
        deleted_store = StoreModel.find_by_name(name)
        if not ItemModel.query.filter_by(store_id=deleted_store.id).all():
            deleted_store.delete_store()
            return {'message': "store '{}' was deleted".format(name)}, 201
        else:
            return {'message': "store '{}' have to be empty".format(name)}, 201


class StoreList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stores', type=dict, action='append')

    @staticmethod
    @jwt_required()
    def get():
        stores = [i.json() for i in StoreModel.query.all()]
        if stores:
            return {'stores': stores}, 201
        return abort(404, message="stores don't exist")

    @staticmethod
    @jwt_required()
    def post():
        new_stores = []
        stores = StoreList.parser.parse_args()['stores']
        if stores:
            for store in stores:
                abort_if_store_exist(store['name'])
            for store in stores:
                new_store = {'name': store['name']}
                new_store = StoreModel(**new_store)
                new_store.add_store()
                new_stores.append(new_store.json())
            return {'new_stores': new_stores}, 201
        return {"message": "stores list mustn't be empty"}, 404

    @staticmethod
    @jwt_required()
    def delete():
        stores = StoreList.parser.parse_args()['stores']
        if stores:
            for store in stores:
                abort_if_store_doesnt_exist(store['name'])
            for store in stores:
                Store.delete(store['name'])
            return {'message': 'stores were deleted'}, 201
        return {"message": "stores list mustn't be empty"}, 404
