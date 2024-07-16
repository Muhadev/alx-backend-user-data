#!/usr/bin/env python3
"""
entry point module
"""
from flask import Flask, request, jsonify
from auth import Auth

# Create a Flask application
app = Flask(__name__)
AUTH = Auth()

# Define a route for "/"
@app.route("/")
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
