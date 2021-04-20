from flask_restful import Resource, reqparse
import sqlite3


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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()
        return {'username': username, 'password': password}
