from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, fields


if __name__ == "flaskpg":
    app = Flask(__name__)
    api = Api(app)

    user_model = api.model(
        'user',
        {
            'email':  fields.String("email@email.com", required=True),
            'password':  fields.String("1234", required=True),
            'age':  fields.Integer(20, required=True),
        }
    )


    app.run(host="127.0.0.1")

    from flaskpg.api_groups.user_api import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix="")
