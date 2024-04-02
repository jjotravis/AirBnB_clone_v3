#!/usr/bin/python3
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, request, abort
from models import storage


cls = City


# @app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route(
    "/states/<string:state_id>/cities", methods=["GET"], strict_slashes=False
)
def get_state_cities(state_id):
    """Retrieves list of cities in a state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    cities = []
    for city in obj.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    obj = storage.get(cls, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a city object"""
    obj = storage.get(cls, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route(
    "/states/<string:state_id>/cities", methods=["POST"], strict_slashes=False
)
def post_city(state_id=None):
    """Creates a city"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj_dict = request.get_json(silent=True)

    if obj_dict is None:
        abort(400, "Not a JSON")
    if "name" not in obj_dict:
        abort(400, "Missing name")
    name = obj_dict["name"]
    obj = cls(name=name, state_id=state_id)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a state object"""
    obj = storage.get(cls, city_id)
    if obj is None:
        abort(404)

    obj_dict = request.get_json(silent=True)
    if obj_dict is None:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if (
            key == "id"
            or key == "state_id"
            or key == "created_at"
            or key == "updated_at"
        ):
            continue
        setattr(obj, key, value)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
