from sqlalchemy import Column, Integer, String
from flaskpg.db.database import Base


class User(Base):
  __tablename__ = "user"

  _id = Column("id", Integer, primary_key=True)
  email = Column("email", String(50), nullable=False)
  password = Column("password", String(50), nullable=False)
  age = Column("age", Integer, nullable=False)

  def __init__(self, email=None, password=None, age=None):
      self.email = email
      self.password = password
      self.age = age
