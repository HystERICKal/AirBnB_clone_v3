#!/usr/bin/python3
"""Make a new flask app here."""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """Return the api status."""
    response = {'status': "OK"}
    return jsonify(response)

