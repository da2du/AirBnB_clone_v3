#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_list(state_id):
    """returns list of cities obj in state"""
    ct_list = []
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    for ct in st.cities:
        ct_list.append(ct.to_dict())
    return jsonify(ct_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_one(city_id):
    """get city"""
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_ct(city_id):
    """Deletes city obj"""
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """creates a new city"""
    http_bd = request.get_json()
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    http_bd['state_id'] = st.id
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    if 'name' not in http_bd.keys():
        abort(400, 'Missing name')
    obj = City(**http_bd)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_ct(state_id):
    """updates a city"""
    http_bd = request.get_json()
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    for key in http_bd.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, http_bd[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
