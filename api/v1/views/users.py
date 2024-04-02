#!/usr/bin/python3
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort
from models import storage


cls = User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id=None):
    """Retrieves user object(s)"""
    if user_id is not None:
        obj = storage.get(cls, user_id)
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())
    else:
        objs = storage.all(cls)
        lst = []
        for obj in objs.values():
            lst.append(obj.to_dict())
        return jsonify(lst)


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_user(user_id):
    """Deletes an user object"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """Creates and posts an user obj"""
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


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a state object"""
    obj = storage.get(cls, user_id)
    if obj is None:
        abort(404)

    obj_dict = request.get_json(silent=True)
    if obj_dict is None:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if (
            key == "id"
            or key == "email"
            or key == "created_at"
            or key == "updated_at"
        ):
            continue
        setattr(obj, key, value)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
