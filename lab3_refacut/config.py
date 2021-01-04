from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import Blueprint

import json
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'biblioteca'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/biblioteca'

mongo = PyMongo(app)
