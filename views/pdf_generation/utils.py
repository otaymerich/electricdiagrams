
from lib2to3.refactor import MultiprocessRefactoringTool
from flask import session
from views.pdf_generation.models import db, Projects, Lines, Proteccions

def organize_house(house: dict):
    line_number = 1
    page = 1
    main_lines = {}
    if "pool" in house.keys():
        pool = add_pool(line_number, page)
        main_lines["pool"] = pool
        line_number += 1
        if line_number > 7:
            page += 1
            line_number = 1
    data = {"data":{
        "proj_description":{
            "project_id": Projects.gen_id(),
            "author": house["author"],
            "title": house["proj_title"],
            "address": house["address"]
            },
        "lines": main_lines 
        }
    }
    create_project(data["data"])
    return "Success"

def add_pool(line_number, page):
    pool = {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": 2,
                "ampere": 40,
                "description": "300mA\nTipo AC-S",
                "page": page},
            "sub_lines":{0:{
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*line_number,
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 20,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_x": 760-100*line_number,
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number}",
                    "description": "Sbq. Piscina",
                    "cable": "H05V-K",
                    "seccion": "2,5mm"}}
            }
    } 
    return pool

def create_project(data: dict):
    proj_desc = data["proj_description"]
    new_project = Projects(proj_desc["project_id"],
                        proj_desc["author"],
                        proj_desc["title"],
                        proj_desc["address"])
    db.session.add(new_project)
    db.session.commit()
    create_lines(data["lines"], proj_desc["project_id"])
    

def create_lines(lines: dict, proj_id: str):
    for line in lines.values():
        create_proteccion(line["head_proteccion"], proj_id)
        print(line["sub_lines"])
        for sub_line in line["sub_lines"].values():
            print(sub_line)
            create_proteccion(sub_line["proteccion"], proj_id)
            new_line = Lines(Lines.gen_id(),
                            proj_id,
                            sub_line["line"]["line_number"],
                            sub_line["line"]["position_x"],
                            sub_line["line"]["description"],
                            sub_line["line"]["cable"],
                            sub_line["line"]["seccion"],
                            sub_line["line"]["page"]
                            )
            db.session.add(new_line)
            db.session.commit()

def create_proteccion(proteccion: dict, proj_id: str):
    new_line = Proteccions(Proteccions.gen_id(),
                    proj_id,
                    proteccion["position_x"],
                    proteccion["position_y"],
                    proteccion["protec_type"],
                    proteccion["pols"],
                    proteccion["ampere"],
                    proteccion["description"],
                    proteccion["page"]
                    )
    db.session.add(new_line)
    db.session.commit()