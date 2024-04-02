#!/usr/bin/python3
"""Create State Objects."""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def combined_states():
    """Return all the available states."""
    reslt = []
    for i in storage.all('State').values():
        reslt.append(i.to_dict())
    return jsonify(reslt)


@app_views.route('states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """Return a single state."""
    county = storage.get('State', state_id)
    if county is None:
        abort(404)
    return jsonify(county.to_dict())


@app_views.route('states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state."""
    county = storage.get("State", state_id)
    if county is None:
        abort(404)
    county.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Make a brand new state."""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    county = State(**request.get_json())
    county.save()
    return make_response(jsonify(county.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Update a state."""
    county = storage.get("State", state_id)
    if county is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'created_at', 'updated_at']:
            setattr(county, i, j)
    county.save()
    return jsonify(county.to_dict())

