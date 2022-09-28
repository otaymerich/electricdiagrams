from db import db
from uuid import uuid4

class Users(db.Model):
    __tablename__ = "users"
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
    id = db.Column(db.String(32), primary_key=True)
    users_id = db.Column(db.String(32), db.ForeignKey("users.id"))
    proj_title = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(43), nullable=False)
    m2 = db.Column(db.Float, nullable=False)
    floors = db.Column(db.Integer)
    pool = db.Column(db.Boolean)
    garden = db.Column(db.Boolean)
    fridge = db.Column(db.Boolean)
    freezer = db.Column(db.Boolean)
    oven = db.Column(db.Boolean)
    vitro_hub = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    boiler = db.Column(db.Boolean)
    aerothermia = db.Column(db.Boolean)
    electric_heater = db.Column(db.Boolean)
    wash_machine = db.Column(db.Boolean)
    dryer = db.Column(db.Boolean)
    iron = db.Column(db.Boolean)
    alarm = db.Column(db.Boolean)
    electronics = db.Column(db.Boolean)
    domotics = db.Column(db.Boolean)
    elec_car = db.Column(db.Boolean)
    solar_panels = db.Column(db.Boolean)
    climate_outdoor_unit = db.Column(db.Interger, nullable=True)
    climate_indoor_unit = db.Column(db.Interger, nullable=True)


    @staticmethod
    def gen_id():
        return uuid4().hex

    def __init__(self, user_id: str, proj_title: str, address: str, m2: float, floors: int, pool: bool, garden: bool, fridge: bool, freezer: bool, oven: bool, vitro_hub: bool, dishwasher: bool, boiler: bool, aerothermia: bool, electric_heater: bool, wash_machine: bool, dryer: bool, iron: bool, alarm: bool, electronics: bool, domotics: bool, elec_car: bool, solar_panels: bool, climate_outdoor_unit=None, climate_indoor_unit=None):
        self.id = self.gen_id()
        self.user_id = user_id
        self.proj_title = proj_title
        self.address = address
        self.m2 = m2
        self.floors = floors
        self.pool = pool
        self.garden = garden
        self.fridge = fridge
        self.freezer = freezer
        self.oven = oven
        self.vitro_hub = vitro_hub
        self.dishwasher = dishwasher
        self.boiler = boiler
        self.aerothermia = aerothermia
        self.electric_heater = electric_heater
        self.wash_machine = wash_machine
        self.dryer = dryer
        self.iron = iron
        self.alarm = alarm
        self.electronics = electronics
        self.domotics = domotics
        self.elec_car = elec_car
        self.solar_panels = solar_panels
        self.climate_outdoor_unit = climate_outdoor_unit
        self.climate_indoor_unit = climate_indoor_unit

