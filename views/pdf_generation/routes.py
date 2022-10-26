from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from auth_obj import Auth
from views.pdf_generation.models import Projects
from views.pdf_generation.shapes2 import create_pdf

pdf = Blueprint("pdf", __name__)

@pdf.route("/project/<house_id>", methods=["POST"])
def t_create_pdf(house_id):
    if request.method == "POST":
        project = Projects.query.filter_by(house_id=house_id).first()
        create_pdf(project)
        return house_id



@pdf.route("/test2")
def t_test():
    project = Projects.query.filter_by(id="d04120e8df734bff90291e34dce40696").first()
    # user = Users.add_user("test1", "test1@email.com", "1234")
    # db.session.add(user)
    # db.session.commit()
    create_pdf(project)
    return "test"
