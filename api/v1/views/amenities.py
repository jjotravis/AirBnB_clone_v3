#!/usr/bin/python3
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request, abort
from models import storage


cls = Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<string:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves amenity object(s)"""
    if amenity_id is not None:
        obj = storage.get(cls, amenity_id)
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())
    else:
        objs = storage.all(cls)
        lst = []
        for obj in objs.values():
            lst.append(obj.to_dict())
        return jsonify(lst)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes an amenity object"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """Creates and posts an amenity obj"""
    obj_dict = request.get_json(silent=True)

    if obj_dict is None:
        abort(400, "Not a JSON")
    if "name" not in obj_dict:
        abort(400, "Missing name")
    name = obj_dict["name"]
    obj = cls(name=name)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a state object"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        abort(404)

    obj_dict = request.get_json(silent=True)
    if obj_dict is None:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(obj, key, value)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
