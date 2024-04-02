#!/usr/bin/python3
"""Create a new view for Amenity objects."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Get all the amenities."""
    facitilies = []
    for i in storage.all("Amenity").values():
        facitilies.append(i.to_dict())
    return jsonify(facitilies)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get single amenity."""
    facility = storage.get("Amenity", amenity_id)
    if facility is None:
        abort(404)
    return jsonify(facility.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity."""
    facility = storage.get("Amenity", amenity_id)
    if facility is None:
        abort(404)
    facility.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Make amenity from scratch."""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    facility = Amenity(**request.get_json())
    facility.save()
    return make_response(jsonify(facility.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update amanity."""
    facility = storage.get("Amenity", amenity_id)
    if facility is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(facility, i, j)
    facility.save()
    return jsonify(facility.to_dict())

