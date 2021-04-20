# from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource, reqparse, abort
import sqlite3


def does_item_exist(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT name, price FROM store WHERE name=?'
    item = list(cursor.execute(query, (name,)))
    connection.commit()
    connection.close()
    if item:
        return True
    return False


def abort_if_item_doesnt_exist(name):
    if not does_item_exist(name):
        return abort(404, message="Item '{}' doesn't exist".format(name))


def abort_if_item_exist(name):
    if does_item_exist(name):
        abort(404, message="Item '{}' have already exist".format(name))


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @staticmethod
    # @jwt_required()
    def get(name):
        abort_if_item_doesnt_exist(name)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT name, price FROM store WHERE name=?'
        item = cursor.execute(query, (name,)).fetchone()
        connection.close()
        return {'name': item[0], 'price': item[1]}

    @staticmethod
    # @jwt_required()
    def post(name):
        abort_if_item_exist(name)
        new_item = {'name': name,
                    'price': Item.parser.parse_args()['price']}
        if str(new_item['price']) != 'None':
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'INSERT INTO store VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, new_item['price']))
            connection.commit()
            connection.close()
            return new_item, 201
        else:
            return abort(404, message='a wrong format of body request. Use {"price": integer}')

    @staticmethod
    # @jwt_required()
    def put(name):
        new_item = {'name': name,
                    'price': Item.parser.parse_args()['price']}
        if new_item['price']:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            if does_item_exist(name):
                query = 'UPDATE store SET price=? WHERE name=?'
                cursor.execute(query, (new_item['price'], name))
                connection.commit()
                connection.close()
                return new_item, 201
            query = 'INSERT INTO store VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, new_item['price']))
            connection.commit()
            connection.close()
            return new_item, 201

    @staticmethod
    # @jwt_required()
    def delete(name):
        abort_if_item_doesnt_exist(name)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM store WHERE name=?'
        item = cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return '', 204


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, action='append')

    @staticmethod
    # @jwt_required()
    def get():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT name, price FROM store'
        items = [{'name': row[0], 'price': row[1]} for row in cursor.execute(query)]
        connection.close()
        return {'items': items}

    @staticmethod
    # @jwt_required()
    def post():
        new_items = []
        items = ItemList.parser.parse_args()['items']
        for item in items:
            if str(item) != 'None':
                abort_if_item_exists(item['name'])
            else:
                return abort(404, message='A wrong format of body request. '
                                          'Use {"items": [{"name": name, "price": price}},]')
        for item in items:
            new_items.append(item)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO store VALUES (NULL, ?, ?)'
        item = cursor.executemany(query, [(item['name'], item['price']) for item in new_items])
        connection.commit()
        connection.close()
        return {'new_items': new_items}, 201
