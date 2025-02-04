#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_rvs(place_id):
    """returns list of reviwes obj in place"""
    ct_list = []
    ct = storage.get(Place, place_id)
    pl = storage.all(Review)
    if not ct:
        abort(404)
    for p in pl.values:
        if p.place_id == ct.id:
            ct_list.append(p)
    return jsonify([p.to_dict() for p in ct_list])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_onepl(place_id):
    """get place"""
    ct = storage.get(Place, place_id)
    if ct is None:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_pli(place_id):
    """Deletes place obj"""
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_pli(city_id):
    """creates a new place"""
    http_bd = request.get_json()
    st = storage.get(City, city_id)
    if st is None:
        abort(404)
    http_bd['city_id'] = st.id
    if not http_bd or not isinstance(http_bd, dict):
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
def update_pli(place_id):
    """updates a place"""
    http_bd = request.get_json()
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    for key in http_bd.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, http_bd[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
