import json
from sqlite3 import IntegrityError
from flask import Flask
from flask import jsonify
from flask import request
from flask_mysqldb import MySQL
from flask import Blueprint
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session(app)
sess.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'geov'
app.config['MYSQL_PASSWORD'] = 'lab_pos'
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    session.pop('role', 'GUEST')
    session.pop('logged_in', 0)
    session.pop('id')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
