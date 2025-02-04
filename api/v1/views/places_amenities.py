#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_ams(place_id):
    """returns list of amenities obj in place"""
    ct_list = []
    ct = storage.get(Place, place_id)
    if not ct:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        am_list = ct.amenities
        return jsonify([a.to_dict() for a in am_list])
    else:
        am = storage.all(Amenity)
        for a in am.values:
            if ct.amenity_ids == a.id:
                ct_list.append(a)
        return jsonify([p.to_dict() for p in ct_list])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_ams(place_id, amenity_id):
    """Deletes amenity obj"""
    obj = storage.get(Place, place_id)
    am_obj = storage.get(Amenity, amenity_id)
    if not obj or not am_obj:
        abort(404)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_pls(city_id):
    """creates a new place"""
    http_bd = request.get_json()
    st = storage.get(City, city_id)
    if st is None:
        abort(404)
    http_bd['city_id'] = st.id
    if not http_bd or type(http_bd) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in http_bd.keys():
        abort(400, 'Missing user_id')
    us = storage.get(User, http_bd['user_id'])
    if not us:
        abort(404)
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    obj = Place(**http_bd)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_pls(place_id):
    """updates a place"""
    http_bd = request.get_json()
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not http_bd or type(http_bd) is not dict:
        abort(400, 'Not a JSON')
    for key in http_bd.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, http_bd[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
