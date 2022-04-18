#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns the number of each objects by type"""
    cl_list = ["Amenity", "City", "Place", "Review", "State", "User"]
    j = {
        "amenities": "0",
        "cities": "0",
        "places": "0",
        "reviews": "0",
        "states": "0",
        "users": "0"}
    i = 0
    for k, v in j.items():
        j[k] = storage.count(cl_list[i])
        i += 1
    return jsonify(j)
