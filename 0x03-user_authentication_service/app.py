#!/usr/bin/env python3
"""
entry point module
"""
from flask import Flask, jsonify, request, abort
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


@app.route('/sessions', methods=['POST'])
def login():
    if not request.form or \
     'email' not in request.form or \
     'password' not in request.form:
        abort(400)

    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    # Get session ID from cookies
    session_id = request.cookies.get('session_id')

    if session_id:
        # Find user with session ID
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            # Destroy session (set session ID to None)
            AUTH.destroy_session(user.id)
            # Redirect to GET / (home page)
            response = make_response(redirect('/'))
            return response
        else:
            # User with session ID not found
            abort(403)
    else:
        # No session ID in cookies
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
