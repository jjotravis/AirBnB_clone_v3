#!/usr/bin/python3
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort
from models import storage


cls = State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id=None):
    """Retrieves state object(s)"""
    if state_id is not None:
        obj = storage.get(cls, state_id)
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())
    else:
        objs = storage.all(cls)
        lst = []
        for obj in objs.values():
            lst.append(obj.to_dict())
        return jsonify(lst)


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a state object"""
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    """Creates and posts state obj"""
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


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a state object"""
    obj = storage.get(cls, state_id)
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
