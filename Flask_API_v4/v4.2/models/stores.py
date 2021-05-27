from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship('ItemModel', backref='store', lazy=True)

    def json(self):
        return {'name': self.name, 'id': self.id}

    @staticmethod
    def find_by_name(name):
        return StoreModel.query.filter_by(name=name).first()

    def add_store(self):
        db.session.add(self)
        db.session.commit()

    def delete_store(self):
        db.session.delete(self)
        db.session.commit()
