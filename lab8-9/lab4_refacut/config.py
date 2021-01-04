import json, base64
from sqlite3 import IntegrityError
from flask import Flask
from flask import jsonify
from flask import request
from flask_mysqldb import MySQL
from flask import Blueprint
from flask import Flask, session
from flask_session import Session
from flask_cors import CORS

# from zeep import Client
# from zeep.transports import Transport
# import pretend

from suds.client import Client


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from jwt.algorithms import get_default_algorithms
get_default_algorithms()

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = base64.b64encode(("\"Te saluta fratele!\"").encode('ascii'))
app.config['JWT_ALGORITHM'] = 'HS512'

CORS(app)

sess = Session(app)
sess.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysqlroot'
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    session.pop('role', 'GUEST')
    session.pop('logged_in', 0)
    session.pop('id', -1)
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
