#!/usr/bin/python
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, request, abort
from models import storage


cls = Place


# @app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route(
    "/cities/<string:city_id>/places", methods=["GET"], strict_slashes=False
)
def get_city_places(city_id):
    """Retrieves list of places in a city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    places = []
    for place in obj.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    obj = storage.get(cls, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """Deletes a place object"""
    obj = storage.get(cls, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route(
    "/cities/<string:city_id>/places", methods=["POST"], strict_slashes=False
)
def post_place(city_id=None):
    """Creates a place"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj_dict = request.get_json(silent=True)

    if obj_dict is None:
        abort(400, "Not a JSON")
    if "name" not in obj_dict:
        abort(400, "Missing name")
    if "user_id" not in obj_dict:
        abort(400, "Missing user_id")

    name = obj_dict["name"]
    user = obj_dict["user_id"]
    obj = storage.get(User, user)
    if obj is None:
        abort(404)
    obj = cls(name=name, city_id=city_id, user_id=user)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    obj = storage.get(cls, place_id)
    if obj is None:
        abort(404)

    obj_dict = request.get_json(silent=True)
    if obj_dict is None:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if (
            key == "id"
            or key == "user_id"
            or key == "city_id"
            or key == "created_at"
            or key == "updated_at"
        ):
            continue
        setattr(obj, key, value)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
