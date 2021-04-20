from flask_restful import Resource, reqparse, abort
import sqlite3


def does_user_exist(username):
    if User.find_by_username(username) is not None:
        return True
    return False


def abort_if_user_doesnt_exist(username):
    if not does_user_exist(username):
        return abort(404, message="User '{}' doesn't exist".format(username))


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id='{self.id}')"

    @staticmethod
    def find_by_username(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        row = cursor.execute(query, (name,)).fetchone()

        connection.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        connection = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        row = cursor.execute(query, (_id,)).fetchone()

        connection.close()

        user = User(*row) if row else None
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    @staticmethod
    def get():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT username, password FROM users'
        users = [{'username': row[0], 'password': row[1]} for row in cursor.execute(query)]
        connection.close()
        return {'users': users}

    @staticmethod
    def post():
        username = UserRegister.parser.parse_args()['username']
        password = UserRegister.parser.parse_args()['password']
        if (str(username) != 'None') and (str(password) != 'None'):
            if does_user_exist(username):
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                query = 'INSERT INTO users VALUES (NULL, ?, ?)'
                cursor.execute(query, (username, password))
                connection.commit()
                connection.close()
                return {'username': username, 'password': password}
            return abort(404, message="User '{}' have already exist".format(username))
        return abort(404, message='A wrong format of body request. Use {"username": string, "password": string}')

    @staticmethod
    # @jwt_required()
    def put():
        new_user = {'username': UserRegister.parser.parse_args()['username'],
                    'password': UserRegister.parser.parse_args()['password']}
        if (str(new_user['username']) != 'None') and (str(new_user['password']) != 'None'):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            if does_user_exist(username):
                query = 'UPDATE users SET password=? WHERE username=?'
                cursor.execute(query, (new_item['username'], new_user['password']))
                connection.commit()
                connection.close()
                return new_user, 201
            query = 'INSERT INTO users VALUES (NULL, ?, ?)'
            cursor.execute(query, (new_user['username'], new_user['password']))
            connection.commit()
            connection.close()
            return new_user, 201
        return abort(404, message='A wrong format of body request. Use {"username": string, "password": string}')

    @staticmethod
    # @jwt_required()
    def delete():
        abort_if_user_doesnt_exist(username)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM users WHERE username=?'
        item = cursor.execute(query, (username,))
        connection.commit()
        connection.close()
        return '', 204
