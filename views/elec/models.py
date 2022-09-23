from db import db
from uuid import uuid4
import datetime as dt

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(40))
    token = db.Column(db.String(43), nullable=True)

    # def __init__(self, id: str, name: str, email: str):
    #     self.id = id
    #     self.name = name
    #     self.email = email
    
    @staticmethod
    def gen_id():
        return uuid4().hex

    def add_user(name: str, email: str, pwd: str):
        return Users(id=Users.gen_id(), name=name, email=email, pwd=pwd)
