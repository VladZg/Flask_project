from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, abort

from models.users import UserModel, db


def does_user_exist(username):
    if UserModel.find_by_username(username) is not None:
        return True
    return False


def abort_if_user_doesnt_exist(username):
    if not does_user_exist(username):
        return abort(404, message="user '{}' doesn't exist".format(username))
    pass


class RegisteredUsers(Resource):

    @staticmethod
    @jwt_required()
    def get():
        users = [i.json() for i in UserModel.query.all()]
        if users:
            return {'users': users}, 201
        return abort(404, message="users don't exist yet")


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password')

    @staticmethod
    @jwt_required()
    def get(username):
        user = UserModel.find_by_username(username)
        if user:
            return {'user': user.json()}, 201
        return abort(404, message="user '{}' doesn't exist".format(username))

    @staticmethod
    def post(username):
        new_user = {'username': username,
                    'password': UserRegister.parser.parse_args()['password']}
        if does_user_exist(username):
            return abort(404, message="user '{}' has already exist".format(username))
        new_user = UserModel(**new_user)
        new_user.add_user()
        return {'new_user': new_user.json()}, 201

    @staticmethod
    @jwt_required()
    def put(username):
        user = {'username': username,
                'password': UserRegister.parser.parse_args()['password']}
        if does_user_exist(username):
            changed_user = UserModel.find_by_username(username)
            changed_user.password = user['password']
            db.session.commit()
            return {'changed_user': changed_user.json()}, 201
        new_user = UserModel(**user)
        new_user.add_user()
        return {'new_user': new_user.json()}, 201

    @staticmethod
    @jwt_required()
    def delete(username):
        deleted_user = UserRegister.parser.parse_args()
        abort_if_user_doesnt_exist(username)
        deleted_user = UserModel.find_by_username(username)
        deleted_user.delete_user()
        return {'message': 'user {} was deleted'.format(username)}, 201
