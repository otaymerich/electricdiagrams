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
    if "garden" in house.keys():
        garden = add_garden(line_number, page)
        main_lines["garden"] = garden
        line_number += 2
    general, line_number, page = add_generallines(house["floors"], house["m2"], line_number, page)
    for i, k in enumerate(general.values(), start=1):
        main_lines[f"general_{i}"] = k
    print(main_lines)
    data = {"data":{
        "proj_description":{
            "project_id": Projects.gen_id(),
            "author": house["author"],
            "title": house["proj_title"],
            "address": house["address"],
            "n_pg": page
            },
        "power_entrance": {},
        "lines": main_lines 
        }
    }
    if "solar_panels" in house.keys():
        data["data"]["power_entrance"]["sub"] = add_solar()
    data["data"]["power_entrance"]["main"] = add_entrance(data["data"])

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
                    "position_y": 760-100*line_number,
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number}",
                    "description": "Sbq. Piscina",
                    "cable": "H05V-K",
                    "seccion": "4mm"}}
            }
    } 
    return pool

def add_generallines(floors, m2, line_number, page):
    if floors == 1 and m2 > 300:
        n = 2
    else:
        n = floors
    general_lines = {}
    for i in range(n):
        general_lines[i] = {"head_proteccion": {
                    "position_x": 139,
                    "position_y": 760-100*line_number,
                    "protec_type": "D",
                    "pols": 2,
                    "ampere": 40,
                    "description": "30mA\nTipo AC",
                    "page": page},
                "sub_lines":{0:{
                    "proteccion":{
                        "position_x": 220,
                        "position_y": 760-100*line_number,
                        "protec_type": "M",
                        "pols": 2,
                        "ampere": 10,
                        "description": "C",
                        "page": page},
                    "line":{
                        "position_y": 760-100*line_number,
                        "pols": 2,
                        "page": page,
                        "line_number": f"L{line_number+(7*(page-1))}",
                        "description": f"Luces interiores {i+1}",
                        "cable": "H05V-K",
                        "pols": 2,
                        "seccion": "1,5mm"}}
                }
        }
        if line_number<7:
            line_number += 1
        else:
            line_number = 1
            page = page +1
        general_lines[i]["sub_lines"][1] = {
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*line_number,
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 10,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*line_number,
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number+(7*(page-1))}",
                    "description": f"Enchufes interiores {i+1}",
                    "cable": "H05V-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
    
        if line_number<7:
            line_number += 1
        else:
            line_number = 1
            page = page +1
        general_lines[i]["sub_lines"][2] = {
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*line_number,
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 10,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*line_number,
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number+(7*(page-1))}",
                    "description": f"Enchufes humedos {i+1}",
                    "cable": "H05V-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
        if line_number<7:
            line_number += 1
        else:
            line_number = 1
            page = page +1   
    return general_lines, line_number, page

def add_garden(line_number, page):
    garden = {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": 2,
                "ampere": 40,
                "description": "30mA\nTipo AC",
                "page": page},
            "sub_lines":{0:{
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*line_number,
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 16,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*line_number,
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number+(7*(page-1))}",
                    "description": "Enchufes exteriores",
                    "cable": "H05V-K",
                    "pols": 2,
                    "seccion": "2,5mm"}},
                    1:{
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*(line_number+1),
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 10,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*(line_number+1),
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{(line_number+1)+(7*(page-1))}",
                    "description": "Luz exterior",
                    "cable": "H05V-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
            }
    } 
    return garden

def add_entrance(data):
    if len(data["lines"])<4:
        ampere = 20
    elif len(data["lines"])<6:
        ampere = 32
    else:
        ampere = 40
    pols = 2
    for line in data["lines"].values():
        if line["head_proteccion"]["pols"] == 4:
                    pols = 4
                    break
    return {"position_x": 48,
            "position_y": 660,
            "protec_type": "M",
            "pols": pols,
            "ampere": ampere,
            "description": "C",
            "page": 1}

def add_solar():
        return {"position_x": 48,
            "position_y": 560,
            "protec_type": "M",
            "pols": 2,
            "ampere": 20,
            "description": "Solar",
            "page": 1}


def create_project(data: dict):
    proj_desc = data["proj_description"]
    print(proj_desc)
    new_project = Projects(proj_desc["project_id"],
                        proj_desc["author"],
                        proj_desc["title"],
                        proj_desc["address"],
                        proj_desc["n_pg"])
    db.session.add(new_project)
    db.session.commit()
    for entrance in data["power_entrance"].values():
        create_proteccion(entrance, proj_desc["project_id"])
    create_lines(data["lines"], proj_desc["project_id"])
    

def create_lines(lines: dict, proj_id: str):
    for line in lines.values():
        create_proteccion(line["head_proteccion"], proj_id)
        for sub_line in line["sub_lines"].values():
            print(sub_line["line"])
            create_proteccion(sub_line["proteccion"], proj_id)
            new_line = Lines(Lines.gen_id(),
                            proj_id,
                            sub_line["line"]["line_number"],
                            sub_line["line"]["position_y"],
                            sub_line["line"]["description"],
                            sub_line["line"]["cable"],
                            sub_line["line"]["pols"],
                            sub_line["line"]["seccion"],
                            sub_line["line"]["page"]
                            )
            db.session.add(new_line)
            db.session.commit()

def create_proteccion(proteccion: dict, proj_id: str):
    new_protec = Proteccions(Proteccions.gen_id(),
                    proj_id,
                    proteccion["position_x"],
                    proteccion["position_y"],
                    proteccion["protec_type"],
                    proteccion["pols"],
                    proteccion["ampere"],
                    proteccion["description"],
                    proteccion["page"]
                    )
    db.session.add(new_protec)
    db.session.commit()