from db import db
from uuid import uuid4


class Projects(db.Model):
    __tablename__ = "projects"
    __bind_key__ = "pdf"
    id = db.Column(db.String(32), primary_key=True)
    author = db.Column(db.String(20))
    title = db.Column(db.String(20))
    address = db.Column(db.String)
    n_pg = db.Column(db.Integer)
    lines = db.relationship("Lines", backref="lines", lazy=True)
    proteccions = db.relationship("Proteccions", backref="proteccions", lazy=True)


    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, project_id: str, author: str, title: str, address: str, n_pg: int):
        self.id = project_id
        self.author = author
        self.title = title
        self.address = address
        self.n_pg = n_pg

class Lines(db.Model):
    __tablename__ = "lines"
    __bind_key__ = "pdf"
    id = db.Column(db.String(32), primary_key=True)
    project_id = db.Column(db.String(32), db.ForeignKey("projects.id"))
    line_number = db.Column(db.Integer)
    position_y = db.Column(db.Float)
    description = db.Column(db.String(20))
    cable = db.Column(db.String(12))
    pols = db.Column(db.Integer)
    seccion = db.Column(db.String(10))
    page = db.Column(db.Integer)


    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, line_id: str, project_id: str, line_number: int, position_y: float, description: str, cable: str, pols: int, seccion: str, page: int):
        self.id = line_id
        self.project_id = project_id
        self.line_number = line_number
        self.position_y = position_y
        self.description = description
        self.cable = cable
        self.pols = pols
        self.seccion = seccion
        self.page = page


class Proteccions(db.Model):
    __tablename__ = "proteccions"
    __bind_key__ = "pdf"
    id = db.Column(db.String(32), primary_key=True)
    project_id = db.Column(db.String(32), db.ForeignKey("projects.id"))
    position_x = db.Column(db.Float)
    position_y = db.Column(db.Float)
    protec_type = db.Column(db.String(12))
    pols = db.Column(db.Integer)
    ampere = db.Column(db.Integer)
    description = db.Column(db.String(20))
    page = db.Column(db.Integer)
    
    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, protec_id:str, project_id: str, position_x: float, position_y: float, protec_type: str, pols: int, ampere: int, description: str, page: int):
        self.id = protec_id
        self.project_id = project_id
        self.position_x = position_x
        self.position_y = position_y
        self.protec_type = protec_type
        self.pols = pols
        self.ampere = ampere
        self.description = description
        self.page = page
