from db import db
from models.item import ItemModel


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data):
        store = cls(id=data.get("id"), name=data.get("name"))
        store.items = [ItemModel.from_dict(item) for item in data.get("items", [])]
        return store
