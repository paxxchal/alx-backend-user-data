#!/usr/bin/env python3
"""
Flask app with user registration endpoint.
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

# Instantiate Auth object
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Return a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user with email and password."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": str(err)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
