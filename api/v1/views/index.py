#!/usr/bin/python3
'''
New flask app is created here
'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """
    Function for checking the api status
    """
    response = {'status': "OK"}
    return jsonify(response)
