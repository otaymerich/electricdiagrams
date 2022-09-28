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

    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, name: str, email: str, pwd: str):
        self.id = self.gen_id()
        self.name = name
        self.email = email
        self.pwd = pwd
    
