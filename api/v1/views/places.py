#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_pls(city_id):
    """returns list of places obj in city"""
    ct_list = []
    ct = storage.get(City, city_id)
    pl = storage.all(Place)
    if not ct:
        abort(404)
    for p in pl.values:
        if p.city_id == ct.id:
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
def delete_pl(place_id):
    """Deletes place obj"""
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_pl(city_id):
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
def update_pl(place_id):
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

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """retrieves all Place objects"""
    http_bd = request.get_json()
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    st = http_bd.get('states', [])
    ct = http_bd.get('cities', [])
    am = http_bd.get('amenities', [])

    if len(st) == len(ct) == 0:
        pl = storage.all('Place').values()
    else:
        pl = []
        for s in st:
            st_obj = storage.get('State', state_id)
            for c in st_obj.cities:
                if c.id not in ct:
                    ct.append(c.id)
        for c in ct:
            ct_obj = storage.get('City', city_id)
            for p in ct_obj.places:
                pl.append(p)
    am_list = []
    am_pl = []
    for a in am:
        am_obj = storage.get('Amenity', amenity_id)
        am_list.append(am_obj)
    for p in pl:
        am_pl.append(p.to_dict())
    return jsonify(am_pl)
