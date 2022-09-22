from flask import Flask
import os
from db import db
from views.elec.routes import elec

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ELEC"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///elec.db"
    app.register_blueprint(elec)
    db.init_app(app)
    return app

def set_db(app):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app = create_app()
    if not os.path.isfile("elec.db"):
        set_db(app)
    app.run(debug=True) 