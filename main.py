from flask import Flask
import os
from db import db
from views.elec.routes import elec
from views.pdf_generation.routes import pdf

from auth_obj import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["SQLALCHEMY_BINDS"] = {
        "elec": "sqlite:///elec.db",
        "pdf": "sqlite:///pdf.db"
    }
    app.register_blueprint(elec)
    app.register_blueprint(pdf)
    db.init_app(app)
    return app

def set_db(app):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app = create_app()
    if not os.path.isfile("elec.db") and not os.path.isfile("pdf.db"):
        set_db(app)
    app.run(debug=True) 