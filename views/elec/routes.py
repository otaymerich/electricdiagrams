from flask import Blueprint, render_template, request, session, redirect, url_for
from auth_obj import Auth
from views.elec.models import db, Users

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
