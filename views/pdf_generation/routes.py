from flask import Blueprint, request, redirect
from auth_obj import Auth
from views.pdf_generation.models import Projects
from views.pdf_generation.shapes2 import create_pdf
# from views.elec.routes import test_auth

pdf = Blueprint("pdf", __name__)

@pdf.route("/project/<house_id>", methods=["POST"])
# @test_auth.auth   !!##Check why when this activated fails!!
def t_create_pdf(house_id):
    if request.method == "POST":
        project = Projects.query.filter_by(house_id=house_id).first()
        create_pdf(project)
    return redirect(f"/projects")

@pdf.route("/test2")
def t_test():
    return "tests also nothing"
