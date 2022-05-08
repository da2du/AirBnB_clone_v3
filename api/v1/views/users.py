#!/usr/bin/python3
"""new view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """Gets all the User"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_usid(user_id=None):
    """returns list of user obj"""
    us_list = storage.get(User, user_id)
    if us_list:
        return jsonify(us_list.to_dict())
    if us_list is None:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_us(user_id=None):
    """Deletes user obj"""
    if user_id is not None:
        obj = storage.get(User, user_id)
        if obj:
            storage.delete(obj)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def new_us():
    """creates a new user"""
    http_bd = request.get_json()
    if not http_bd or not isinstance(http_bd, dict):
        abort(400, 'Not a JSON')
    if 'email' not in http_bd.keys():
        abort(400, 'Missing email')
    if 'password' not in http_bd.keys():
        abort(400, 'Missing password')
    obj = User(**http_bd)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_us(user_id):
    """updates a user"""
    if user_id is None:
        abort(404)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, description='Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
