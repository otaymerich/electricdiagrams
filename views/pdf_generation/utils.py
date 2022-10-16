
from flask import session
from views.pdf_generation.models import db, Projects, Lines, Proteccions

def organize_house(house: dict):
    line_number = 1
    page = 1
    main_lines = {}
    if house["pool"]:
        main_lines["pool"] = {
            "head_proteccion": {
                
                },
            "sub_lines": {
                
                }
            }

    data = {"data":{
        "proj_description":{
            "author": house["author"],
            "title": house["proj_title"],
            "adress": house["address"]
            },
        "lines":{

            }  
        }
    }


def create_project(house: dict):
    new_project = Projects(house["author"],
                        house["proj_title"],
                        house["address"])
    db.session.add(new_project)
    db.session.commit()
    

def create_line(line: dict):
    pass

def create_protecction(portecction: dict):
    pass