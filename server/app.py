from flask import Flask, jsonify, request
from flask_migrate import Migrate
from server.extensions import db, ma

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# import models so Flask-Migrate can detect table metadata
from server import models

# initialize Flask-Migrate with the app and database
migrate = Migrate(app, db)

# Routes here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
