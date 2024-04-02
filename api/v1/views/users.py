#!/usr/bin/python3
"""Create a new view for User object."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Fetch all users."""
    cust = []
    for i in storage.all("User").values():
        cust.append(i.to_dict())
    return jsonify(cust)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Fetch a single user."""
    s_cust = storage.get("User", user_id)
    if s_cust is None:
        abort(404)
    return jsonify(s_cust.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user."""
    s_cust = storage.get("User", user_id)
    if s_cust is None:
        abort(404)
    s_cust.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Make a user from scratch."""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    s_cust = User(**request.get_json())
    s_cust.save()
    return make_response(jsonify(s_cust.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update a user."""
    s_cust = storage.get("User", user_id)
    if s_cust is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(s_cust, i, j)
    s_cust.save()
    return jsonify(s_cust.to_dict())

