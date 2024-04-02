#!/usr/bin/python3
"""Handle starting of api."""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Return JSON status."""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """Retrieve number of each obj by type."""
    classes = {
        'amenities': 'Amenity',
        'cities': 'City',
        'places': 'Place',
        'reviews': 'Review',
        'states': 'State',
        'users': 'User'
    }
    reslt = {}
    for i, j in classes.items():
        reslt[i] = storage.count(j)
    return jsonify(reslt)


if __name__ == '__main__':
    pass

