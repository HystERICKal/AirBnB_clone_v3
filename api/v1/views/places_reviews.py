#!/usr/bin/python3
"""Create a new view for Review object."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Fetch all the reviews."""
    mahli = storage.get("Place", place_id)
    if mahli is None:
        abort(404)
    maono = []
    for i in mahli.reviews:
        maono.append(i.to_dict())
    return jsonify(maono)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Fetch a songle review."""
    kiono = storage.get("Review", review_id)
    if kiono is None:
        abort(404)
    return jsonify(kiono.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete required review."""
    kiono = storage.get("Review", review_id)
    if kiono is None:
        abort(404)
    kiono.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Make a review from scratch."""
    mahli = storage.get("Place", place_id)
    if mahli is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    temp_k = request.get_json()
    if 'user_id' not in temp_k:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    msee = storage.get("User", temp_k['user_id'])
    if msee is None:
        abort(404)
    if 'text' not in temp_k:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    temp_k['place_id'] = place_id
    kiono = Review(**temp_k)
    kiono.save()
    return make_response(jsonify(kiono.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Return updated review."""
    kiono = storage.get("Review", review_id)
    if kiono is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(kiono, i, j)
    kiono.save()
    return jsonify(kiono.to_dict())

