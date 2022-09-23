from flask import Blueprint, render_template, request, session
from auth_obj import Auth
from views.elec.models import db, Users

elec = Blueprint("elec", __name__)
test_auth = Auth(session, Users, "elec.t_login", "elec.home", request, db)

@elec.route("/", methods=["GET", "POST"])
@test_auth.auth
def home():
    return render_template("base.html")

@elec.route("/login", methods=["GET", "POST"])
@test_auth.login_check
def t_login():
    return render_template("login.html")


@elec.route("/test")
def t_test():
    user = Users.add_user("test1", "test1@email.com", "1234")
    db.session.add(user)
    db.session.commit()
    return "test"
if __name__ == "__main__":
    print(type(request))