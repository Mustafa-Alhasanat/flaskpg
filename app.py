from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields, reqparse
from pydantic import BaseModel
from flask_pydantic import validate


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


class Account(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(20))
    age = db.Column("age", db.Integer)

    def __init__(self, email=None, password=None, age=None):
        self.email = email
        self.password = password
        self.age = age


class Body(BaseModel):
  email: str
  password: str
  age: int


@api.route("/users/<int:id>")
class User(Resource):
    def get(self, id):
        try:
            user = Account.query.filter_by(_id=id).first() 

            response_data = {
                "id": user._id,
                "email": user.email,
                "password": user.password,
                "age": user.age
            } 

            return response_data, 200
        
        except:
            return "Not found", 400

    @api.expect(user_model)
    @validate()
    def put(self, id, body: Body):
        try:
            user = Account.query.filter_by(_id=id).first()
            for key in ["email", "password", "age"]:
                exec(f"setattr(user, key, body.{key})")

            db.session.commit()

            response_data = {
                "id": user._id,
                "email": user.email,
                "password": user.password,
                "age": user.age
            } 

            return response_data, 200
        
        except:
            return "server error", 500

    def delete(self, id):
        try:
            user = Account.query.filter_by(_id=id)

            user.delete()
            db.session.commit()

            return "user has been deleted !", 200
        
        except:
            return "server error", 500


@api.route("/users/")
class Users(Resource):
    def get(self):
        try:
            all_users = Account.query.all()

            response_data = { user._id : \
                {
                    "email": user.email,
                    "password": user.password,
                    "age": user.age
                } \
                for user in all_users}

            return response_data, 200
        
        except:
            return "server error", 500

    @api.expect(user_model)
    @validate()
    def post(self, body: Body):
        try:
            email = body.email
            password = body.password
            age = body.age

            user = Account(email, password, age)
            db.session.add(user)
            db.session.commit()
    
            response_data = {
                "email": body.email,
                "password": body.password,
                "age": body.age    
            }

            return response_data, 200
    
        except:  
            return "Server Error", 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
