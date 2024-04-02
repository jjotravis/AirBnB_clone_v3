#!/usr/bin/python3
"""Flask for AirBnB clone api"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def teardown(exception):
    """Calls storage.close"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """error 404"""
    return make_response(jsonify({"error" : "Not found"}), 404)

if __name__ == "__main__":
    p = os.getenv("HBNB_API_PORT", "5000")
    h = os.getenv("HBNB_API_HOST", "0.0.0.0")
    app.run(host=h, port=p, threaded=True)