#!/usr/bin/python3
"""Create a new view for Place objects."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Fetch all the places."""
    mtaa = storage.get("City", city_id)
    if mtaa is None:
        abort(404)
    mabase = []
    for i in mtaa.places:
        mabase.append(i.to_dict())
    return jsonify(mabase)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Fetch a single place."""
    kibase = storage.get("Place", place_id)
    if kibase is None:
        abort(404)
    return jsonify(kibase.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place."""
    kibase = storage.get("Place", place_id)
    if kibase is None:
        abort(404)
    kibase.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Make a place from scratch."""
    mtaa = storage.get("City", city_id)
    if mtaa is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    temp_k = request.get_json()
    if 'user_id' not in temp_k:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    msee = storage.get("User", temp_k['user_id'])
    if msee is None:
        abort(404)
    if 'name' not in temp_k:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    temp_k['city_id'] = city_id
    kibase = Place(**temp_k)
    kibase.save()
    return make_response(jsonify(kibase.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updtade a place."""
    kibase = storage.get("Place", place_id)
    if kibase is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for i, j in request.get_json().items():
        if i not in ['id', 'user_id', 'city_id', 'created_at',
                     'updated_at']:
            setattr(kibase, i, j)
    kibase.save()
    return jsonify(kibase.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Search a place."""
    if request.get_json() is not None:
        kitu_p = request.get_json()
        macounti = kitu_p.get('states', [])
        counti = kitu_p.get('cities', [])
        vifaa = kitu_p.get('amenities', [])
        tumiavifaa = []
        for i in vifaa:
            kifaa = storage.get('Amenity', i)
            if kifaa:
                tumiavifaa.append(kifaa)
        if macounti == counti == []:
            mabase = storage.all('Place').values()
        else:
            mabase = []
            for j in macounti:
                mahli = storage.get('State', j)
                mahli_noma = mahli.cities
                for k in mahli_noma:
                    if k.id not in counti:
                        counti.append(k.id)
            for lilo in counti:
                mtaa = storage.get('City', lilo)
                for m in mtaa.places:
                    mabase.append(m)
        mahli_tru = []
        for n in mabase:
            mahli_vifaaa = n.amenities
            mahli_tru.append(n.to_dict())
            for p in tumiavifaa:
                if p not in mahli_vifaaa:
                    mahli_tru.pop()
                    break
        return jsonify(mahli_tru)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

