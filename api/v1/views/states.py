#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get(state_id=None):
    """returns list of state obj"""
    if state_id is None:
        st_list = []
        for st in storage.all(State).values():
            st_list.append(st.to_dict())
        return jsonify(st_list)
    else:
        st_list = storage.get(State, state_id)
        if st_list is None:
            abort(404)
        return jsonify(st_list.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete(state_id):
    """Deletes state obj"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_statw():
    """creates a new state"""
    http_bd = request.get_json()
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    if 'name' not in http_bd.keys():
        abort(400, 'Missing name')
    obj = State(**http_bd)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_st(state_id):
    """updates a state"""
    http_bd = request.get_json()
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if http_bd is None:
        abort(400, 'Not a JSON')
    for key in http_bd.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, http_bd[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
