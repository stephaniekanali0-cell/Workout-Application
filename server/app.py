from flask import Flask, jsonify, request
from flask_migrate import Migrate
from extensions import db, ma

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize Flask-Migrate with the app and database
migrate = Migrate(app, db)

db.init_app(app)

# Routes here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
