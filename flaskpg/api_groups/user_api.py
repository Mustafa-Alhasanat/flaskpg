from flask import Blueprint
from flask_restx import Resource
from flask_pydantic import validate

from flaskpg.app import api, user_model
from flaskpg.db.database import db_session as db
from flaskpg.db.db import User
from flaskpg.models.user_request import UserRequest


users_blueprint = Blueprint("users", __name__, static_folder="static", template_folder="templates")


@api.route("/users/<int:id>")
class UserController(Resource):
    def get(self, id):
        user = User.query.filter_by(_id=id).first() 

        if user is None:
            return "User not found", 404

        response_data = {
            "id": user._id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "age": user.age
        } 

        return response_data, 200
        

    @api.expect(user_model)
    @validate()
    def put(self, id, body: UserRequest):
        user = User.query.filter_by(_id=id).first()
        
        if user is None:
            return "User not found", 404
        
        for key in ["email", "password", "age"]:
            exec(f"setattr(user, key, body.{key})")

        db.commit()

        response_data = {
            "id": user._id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "age": user.age
        } 

        return response_data, 200
    

    def delete(self, id):
        user = User.query.filter_by(_id=id)

        user.delete()
        db.commit()

        return "user has been deleted !", 200
    

@api.route("/users/")
class UsersController(Resource):
    def get(self):
        all_users = User.query.all()

        if all_users is None:
            return "User not found", 404

        response_data = { user._id : \
            {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "age": user.age
            } \
            for user in all_users}

        return response_data, 200
    

    @api.expect(user_model)
    @validate()
    def post(self, body: UserRequest):
        
        if body is None:
            return "Body not found", 404

        name = body.name
        email = body.email
        password = body.password
        age = body.age

        user = User(name, email, password, age)
        
        db.add(user)
        db.commit()

        response_data = {
            "name": body.name,
            "email": body.email,
            "password": body.password,
            "age": body.age    
        }

        return response_data, 200

