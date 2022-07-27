from flask import Blueprint
from flask_restx import Resource
from flask_pydantic import validate

from flaskpg import api, user_model
from flaskpg.db.database import db_session as db
from flaskpg.db.db import User
from flaskpg.models.user_request import UserRequest


users_blueprint = Blueprint("account", __name__, static_folder="static", template_folder="templates")


@api.route("/users/<int:id>")
class UserController(Resource):
    def get(self, id):
        try:
            user = User.query.filter_by(_id=id).first() 

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
    def put(self, id, body: UserRequest):
        try:
            user = User.query.filter_by(_id=id).first()
            for key in ["email", "password", "age"]:
                exec(f"setattr(user, key, body.{key})")

            db.commit()

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
            user = User.query.filter_by(_id=id)

            user.delete()
            db.commit()

            return "user has been deleted !", 200
        
        except:
            return "server error", 500


@api.route("/users/")
class UsersController(Resource):
    def get(self):
        try:
            all_users = User.query.all()

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
    def post(self, body: UserRequest):
        try:
            email = body.email
            password = body.password
            age = body.age

            user = User(email, password, age)
            db.add(user)
            db.commit()
    
            response_data = {
                "email": body.email,
                "password": body.password,
                "age": body.age    
            }

            return response_data, 200
    
        except:  
            return "Server Error", 500

