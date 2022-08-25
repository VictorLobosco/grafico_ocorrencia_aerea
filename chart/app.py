from flask import Flask, jsonify, render_template, request
from werkzeug.serving import run_simple
import json
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def home():
    return render_template('h.html')



run_simple('localhost', 5005, app, use_reloader=True)

