#!/usr/bin/python3
"""Create a new view for City objects."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Fetch all the cities."""
    county = storage.get("State", state_id)
    if county is None:
        abort(404)
    mamtaa = []
    for i in county.cities:
        mamtaa.append(i.to_dict())
    return jsonify(mamtaa)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Fetch just one city."""
    mtaa = storage.get("City", city_id)
    if mtaa is None:
        abort(404)
    return jsonify(mtaa.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete required city."""
    mtaa = storage.get("City", city_id)
    if mtaa is None:
        abort(404)
    mtaa.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Make a city from scratch."""
    county = storage.get("State", state_id)
    if county is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    temp = request.get_json()
    temp['state_id'] = state_id
    mtaa = City(**temp)
    mtaa.save()
    return make_response(jsonify(mtaa.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update city stuff."""
    mtaa = storage.get("City", city_id)
    if mtaa is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(mtaa, i, j)
    mtaa.save()
    return jsonify(mtaa.to_dict())

