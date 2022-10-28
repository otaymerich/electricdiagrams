from db import db
from uuid import uuid4

class Users(db.Model):
    __tablename__ = "users"
    __bind_key__ = "elec"
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(40))
    token = db.Column(db.String(43), nullable=True)
    houses = db.relationship("House", backref="houses", lazy=True)

    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, name: str, email: str, pwd: str):
        self.id = self.gen_id()
        self.name = name
        self.email = email
        self.pwd = pwd
    
class House(db.Model):
    __tablename__ = "houses"
    __bind_key__ = "elec"
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"))
    proj_title = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String, nullable=False)
    m2 = db.Column(db.Float, nullable=False)
    floors = db.Column(db.Integer)
    heating_system = db.Column(db.String)
    fridge = db.Column(db.Boolean)
    freezer = db.Column(db.Boolean)
    oven = db.Column(db.Boolean)
    vitro_hub = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    wash_machine = db.Column(db.Boolean)
    dryer = db.Column(db.Boolean)
    iron = db.Column(db.Boolean)
    climate_outdoor_unit = db.Column(db.Integer, nullable=True)
    climate_indoor_unit = db.Column(db.Integer, nullable=True)
    alarm = db.Column(db.Boolean)
    electronics = db.Column(db.Boolean)
    domotics = db.Column(db.Boolean)
    elec_car = db.Column(db.Boolean)
    solar_panels = db.Column(db.Boolean)
    pool = db.Column(db.Boolean)
    garden = db.Column(db.Boolean)


    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, user_id: str, new_house: dict):
        self.id = self.gen_id()
        self.user_id = user_id
        self.proj_title = new_house["proj_title"]
        self.address = new_house["address"]
        self.m2 = new_house["m2"]
        self.floors = new_house["floors"]
        self.pool = new_house["pool"]
        self.garden = new_house["garden"]
        self.fridge = new_house["fridge"]
        self.freezer = new_house["freezer"]
        self.oven = new_house["oven"]
        self.vitro_hub = new_house["vitro_hub"]
        self.dishwasher = new_house["dishwasher"]
        self.heating_system = new_house["heating_system"]
        self.wash_machine = new_house["wash_machine"]
        self.dryer = new_house["dryer"]
        self.iron = new_house["iron"]
        self.alarm = new_house["alarm"]
        self.electronics = new_house["electronics"]
        self.domotics = new_house["domotics"]
        self.elec_car = new_house["elec_car"]
        self.solar_panels = new_house["solar_panels"]
        self.climate_outdoor_unit = new_house["climate_outdoor_unit"]
        self.climate_indoor_unit = new_house["climate_indoor_unit"]

    def project(self) -> dict:
        house = {"author": Users.query.filter_by(id=self.user_id).first().name}
        for k,v in vars(self).items():
            if k[0] != "_" and k != "user_id" and v != None: #revisar
                house[k] = v
        return house
    
    def public(self) -> dict:
        return {"Proj. title": self.proj_title,
                "Address": self.address,
                "Square meeters": self.m2,
                "Floors": self.floors,
                "Download project": self.id}
