#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_am(amenity_id=None):
    """returns list of amenity obj"""
    if amenity_id is None:
        am_list = []
        for am in storage.all(Amenity).values():
            am_list.append(am.to_dict())
        return jsonify(am_list)
    else:
        am_list = storage.get(Amenity, amenity_id)
        if am_list is None:
            abort(404)
        return jsonify(am_list.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_am(amenity_id):
    """Deletes amenity obj"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def new_am():
    """creates a new amenity"""
    http_bd = request.get_json()
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    if 'name' not in http_bd.keys():
        abort(400, 'Missing name')
    obj = Amenity(**http_bd)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_am(amenity_id):
    """updates a amenity"""
    http_bd = request.get_json()
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    for key in http_bd.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, http_bd[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
