from flask import Blueprint, render_template, request, session, redirect, url_for
from auth_obj import Auth
from views.elec.models import db, Users, House

elec = Blueprint("elec", __name__)
test_auth = Auth(session, Users, "elec.t_login", "elec.home", request, db)

'''
HOME
'''
@elec.route("/", methods=["GET", "POST"])
@test_auth.auth
def home():
    return render_template("base.html")

'''
LOGIN/LOGOUT
'''
@elec.route("/login", methods=["GET", "POST"])
@test_auth.login_check
def t_login():
    if request.method == "POST":
        rf = request.form
        new_user = Users(rf["name"], rf["email"], Auth.encrypt_psw(rf["pwd"]))
        db.session.add(new_user)
        db.session.commit()
    return render_template("login.html")

@elec.route("/newproject", methods=["GET", "POST"])
@test_auth.auth
def t_new_project():
    if request.method == "POST":
        rf = request.form
        new_house = (session["id"],
                    rf.get("proj_title"),
                    rf.get("address"),
                    rf.get("m2"),
                    rf.get("floors"),
                    # rf.get("pool"),
                    # rf.get("garden"),
                    rf.get("fridge"),
                    # rf.get("freezer"),
                    # rf.get("oven"),
                    # rf.get("vitro_hub"),
                    # rf.get("heating_system"),
                    # rf.get(rf.get("wash_machine"),
                    # rf.get("dryer"),
                    # rf.get("iron"),
                    # rf.get("out_units"),
                    # rf.get("in_units"),
                    # rf.get("alarm"),
                    # rf.get("electronics"),
                    # rf.get("domotics"),
                    # rf.get("elec_car"),
                    # rf.get("solar_panels")
        )
        new_house = (*dict(rf).values(),)
        print(new_house)
    return render_template("new_project.html")


@elec.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for("elec.t_login"))

@elec.route("/test")
def t_test():
    # user = Users.add_user("test1", "test1@email.com", "1234")
    # db.session.add(user)
    # db.session.commit()
    return "test"
