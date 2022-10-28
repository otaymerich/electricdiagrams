from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from auth_obj import Auth
from views.elec.models import db, Users, House
from views.pdf_generation.utils import organize_house
import base64

elec = Blueprint("elec", __name__)
test_auth = Auth(session, Users, "elec.t_login", "elec.home", request, db)

'''
HOME PAGE
'''
@elec.route("/", methods=["GET", "POST"])
@test_auth.auth
def home():
    return render_template("base.html", instructions = True)

'''
LOGIN/LOGOUT
'''
@elec.route("/login", methods=["GET", "POST"])
@test_auth.login_check
def t_login():
    if request.method == "POST":
        rf = request.form
        email = Users.query.filter_by(email=rf["email"]).first()
        if not email:
            new_user = Users(rf["name"], rf["email"], Auth.encrypt_psw(rf["pwd"]))
            db.session.add(new_user)
            db.session.commit()
        else:
            return render_template("login.html", message="**The user you tryed to create already exists**")
    return render_template("login.html", notloged = True)

@elec.route("/newproject", methods=["GET", "POST"])
@test_auth.auth
def t_new_project():
    if request.method == "POST":
        rf = request.form
        new_house = {}
        form_values = ["proj_title", "address",  "m2", "floors", "heating_system", "pool", "garden", "fridge", "freezer", "oven", "vitro_hub", "dishwasher", "wash_machine", "dryer", "iron", "climate_outdoor_unit", "climate_indoor_unit", "alarm", "electronics", "domotics", "elec_car", "solar_panels"]
        for name in form_values:
            new_house[name] = True if rf.get(name)=="True" else rf.get(name)
        house = House(session.get("id"), new_house)
        db.session.add(house)
        db.session.commit()
        organize_house(house.project())
        return redirect(f"/projects")
    return render_template("new_project.html")

@elec.route("/projects")
@test_auth.auth
def t_show_projects():
    user = Users.query.filter_by(id=session.get("id")).first()
    houses = list(map(lambda roomie: roomie.public(), user.houses))
    return render_template("table.html", elements=houses)

@elec.route("/profile", methods=["GET", "POST"])
@test_auth.auth
def t_profile():
    user = Users.query.filter_by(id=session.get("id")).first()
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            user.name = name
        email = request.form.get("email")
        if email:
            user.email = email
        img = request.files.get("logo")
        if img:
            img_extension = img.filename.rsplit(".")[-1]
            if img_extension == "png":
                img.save(f"./static/logos/{session.get('id')}_logo.png")
        db.session.add(user)
        db.session.commit()
    logo = f"./static/logos/{user.id}_logo.png" #Maybe I should add some kind of size regulation for the card not to be gigantic
    return render_template("card.html", name=user.name, email=user.email, logo=logo)

@elec.route("/delate/<house_id>", methods=["POST"])
@test_auth.auth
def t_delate_house(house_id):
    if request.method == "POST":
        house = db.session.query(House).filter(House.id==house_id).first()
        db.session.delete(house)
        db.session.commit()
    return redirect(f"/delate_project/{house_id}")

@elec.route("/logout")
def log_out():
    session.clear()
    res = make_response(redirect(url_for("elec.t_login")))
    res.delete_cookie("name")
    return res

@elec.route("/test")
def t_test():
    return "tests nothing"
