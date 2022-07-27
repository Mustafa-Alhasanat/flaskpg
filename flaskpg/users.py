from flask import Blueprint
from flask_restx import Resource
from flask_pydantic import validate

from flaskpg import api, user_model, db
from flaskpg.account import Account, Body


users_blueprint = Blueprint("account", __name__, static_folder="static", template_folder="templates")


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

