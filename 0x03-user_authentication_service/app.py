#!/usr/bin/env python3
"""
entry point module
"""
from flask import Flask, jsonify

# Create a Flask application
app = Flask(__name__)

# Define a route for "/"
@app.route("/")
def index():
    return jsonify({"message": "Bienvenue"})

# Run the Flask app if executed directly


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
