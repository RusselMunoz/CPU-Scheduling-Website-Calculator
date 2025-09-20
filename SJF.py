from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve the HTML file
@app.route("/")
def index():
    with open('index.html', 'r') as file:
        return file.read()

@app.route("/fcfs", methods=["POST"])
def fcfs():
    try:
        data = request.json