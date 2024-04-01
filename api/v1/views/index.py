#!/usr/bin/python3
'''api connection begins with this file'''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """This route returns a JSON status"""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """retruns the number of each object by type"""
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
