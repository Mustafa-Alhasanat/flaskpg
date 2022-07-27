from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, fields

import os
from dotenv import load_dotenv

load_dotenv()
FLASK_HOST = os.getenv('FLASK_HOST')

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://mustafa:hasanat123@localhost/accounts'
db = SQLAlchemy(app)

user_model = api.model(
    'user',
    {
        'email':  fields.String("email@email.com", required=True),
        'password':  fields.String("1234", required=True),
        'age':  fields.Integer(20, required=True),
    }
)


app.run(host=f"{FLASK_HOST}")

from flaskpg.users import users_blueprint
app.register_blueprint(users_blueprint, url_prefix="")


