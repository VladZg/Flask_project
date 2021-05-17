from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'username': self.username, 'password': self.password}

    @staticmethod
    def find_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(_id):
        return UserModel.query.filter_by(id=_id).first()

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
