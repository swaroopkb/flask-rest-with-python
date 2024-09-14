import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import StoreModel
from schemas import StoreSchema
from redis_client import set_redis_value, get_redis_value


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        stored_store = get_redis_value(store_id)
        print("Retrieving from cache", json.loads(stored_store))
        if stored_store:
            model_dict = json.loads(stored_store)

            return StoreModel.from_dict(model_dict)
        store = StoreModel.query.get_or_404(store_id)

        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Item Deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
            if store:
                print("Storing to cache")
                store_json = json.dumps(store.to_dict())
                set_redis_value(store.id, store_json)
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store")
        return store, 201
