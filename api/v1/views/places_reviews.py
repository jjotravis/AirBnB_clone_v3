#!/usr/bin/python
"""Handles RESTFul API action for state objects"""

from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, request, abort
from models import storage


cls = Review


# @app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route(
    "/places/<string:place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_place_review(place_id):
    """Retrieves list Review of places """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    reviews = []
    for review in obj.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    obj = storage.get(cls, review_id_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review(review_id):
    """Deletes a place object"""
    obj = storage.get(cls, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route(
    "/places/<string:place_id>/reviews", methods=["POST"], strict_slashes=False
)
def post_review(place_id=None):
    """Creates a Review"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj_dict = request.get_json(silent=True)

    if obj_dict is None:
        abort(400, "Not a JSON")
    if "text" not in obj_dict:
        abort(400, "Missing text")
    if "user_id" not in obj_dict:
        abort(400, "Missing user_id")

    text = obj_dict["text"]
    user = obj_dict["user_id"]
    obj = storage.get(User, user)
    if obj is None:
        abort(404)
    obj = cls(text=text, place_id=place_id, user_id=user)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    obj = storage.get(cls, review_id_id)
    if obj is None:
        abort(404)

    obj_dict = request.get_json(silent=True)
    if obj_dict is None:
        abort(400, "Not a JSON")
    for key, value in obj_dict.items():
        if (
            key == "id"
            or key == "user_id"
            or key == "plce_id"
            or key == "created_at"
            or key == "updated_at"
        ):
            continue
        setattr(obj, key, value)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
