from db import db
from models.stores import StoreModel


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    def json(self):
        return {'name': self.name, 'price': self.price, 'store': StoreModel.query.filter_by(id=self.store_id).first().name}

    @staticmethod
    def find_by_name(name):
        return ItemModel.query.filter_by(name=name).first()

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
