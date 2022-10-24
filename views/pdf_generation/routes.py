from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from auth_obj import Auth
from views.pdf_generation.models import Projects
from views.pdf_generation.shapes2 import create_pdf

pdf = Blueprint("pdf", __name__)

@pdf.route("/test2")
def t_test():
    project = Projects.query.filter_by(id="c9e379f17c144e0086bf50780bb7f125").first()
    # user = Users.add_user("test1", "test1@email.com", "1234")
    # db.session.add(user)
    # db.session.commit()
    create_pdf(project)
    return "test"
