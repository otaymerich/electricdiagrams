from flask import Blueprint, request, redirect
# from auth_obj import Auth
from views.pdf_generation.models import Lines, Projects, Proteccions, db
from views.pdf_generation.shapes2 import create_pdf
# from views.elec.routes import test_auth

pdf = Blueprint("pdf", __name__)

@pdf.route("/project/<house_id>", methods=["POST"])
# @test_auth.auth   !!##Check why when this activated fails!!
def t_create_pdf(house_id: str):
    if request.method == "POST":
        project = Projects.query.filter_by(house_id=house_id).first()
        create_pdf(project)
    return redirect(f"/projects")

@pdf.route("/delate_project/<house_id>") #if i put the decorator @test_auth.auth gives error??
def t_delate_project(house_id: str):
    project = Projects.query.filter_by(house_id=house_id).first()
    lines = Lines.query.filter_by(project_id=project.id).all()
    for line in lines:
        db.session.delete(line)
    proteccions = Proteccions.query.filter_by(project_id=project.id).all()
    for protec in proteccions:
        db.session.delete(protec)
    db.session.delete(project)
    db.session.commit()
    return redirect(f"/projects")

@pdf.route("/test2")
def t_test():
    return "tests also nothing"
