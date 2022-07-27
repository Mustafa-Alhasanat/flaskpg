from pydantic import BaseModel

from flaskpg import db


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
