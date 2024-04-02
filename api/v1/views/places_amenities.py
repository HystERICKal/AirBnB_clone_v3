#!/usr/bin/python3
"""Create a new view for Place and Amenity."""

from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenities(place_id):
    """Fetch all amenities."""
    the_place = storage.get("Place", str(place_id))
    vifaa_zote = []

    if the_place is None:
        abort(404)

    for i in the_place.amenities:
        vifaa_zote.append(i.to_json())

    return jsonify(vifaa_zote)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def the_unlinker(place_id, amenity_id):
    """Unlink amenities from place obk=jects."""
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    the_place = storage.get("Place", place_id)
    countr = 0

    for i in the_place.amenities:
        if str(i.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                the_place.amenities.remove(i)
            else:
                the_place.amenity_ids.remove(i.id)
            the_place.save()
            countr = 1
            break

    if countr == 0:
        abort(404)
    else:
        temp_r = jsonify({})
        temp_r.status_code = 201
        return temp_r


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def the_linker(place_id, amenity_id):
    """Link amenities and place objects."""
    the_place = storage.get("Place", str(place_id))
    the_kifaa = storage.get("Amenity", str(amenity_id))
    pata_this = None

    if not the_place or not the_kifaa:
        abort(404)

    for i in the_place.amenities:
        if str(i.id) == amenity_id:
            pata_this = i
            break

    if pata_this is not None:
        return jsonify(pata_this.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        the_place.amenities.append(the_kifaa)
    else:
        the_place.amenities = the_kifaa

    the_place.save()

    temp_r = jsonify(the_kifaa.to_json())
    temp_r.status_code = 201

    return temp_r

