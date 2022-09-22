from flask import Blueprint, render_template, request, session, url_for, redirect

elec = Blueprint("elec", __name__)

@elec.route("/", methods=["GET", "POST"])
def home():
    return render_template("base.html")