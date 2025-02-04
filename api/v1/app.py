#!/usr/bin/python3
"""Flask app"""

from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tr(ex):
    """method that closes storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error in json"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host, port, threaded=True)
