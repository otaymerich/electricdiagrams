from lib2to3.refactor import MultiprocessRefactoringTool
from views.pdf_generation.models import db, Projects, Lines, Proteccions

def actualize_line_page(line_number: int, page: int):
    if line_number<7:
            line_number += 1
    else:
        line_number = 1
        page = page +1
    return line_number, page

def organize_house(house: dict):
    line_number = 1
    page = 1
    main_lines = {}
    keys = house.keys()
    if "pool" in keys:
        pool = add_pool(line_number, page)
        main_lines["pool"] = pool
        line_number, page = actualize_line_page(line_number, page)
    if "garden" in keys:
        garden, line_number, page = add_garden(line_number, page)
        main_lines["garden"] = garden
    print(house)
    print(house["heating_system"])
    heating_system, line_number, page = add_heating_system(house["heating_system"], line_number, page)
    main_lines["heating_system"] = heating_system
    general, line_number, page = add_generallines(house["floors"], house["m2"], line_number, page)
    for i, k in enumerate(general.values(), start=1):
        main_lines[f"general_{i}"] = k
    cleaning = list(filter(lambda key: key if key == "wash_machine" or key == "iron" or key == "dryer" else None, keys))
    if len(cleaning) > 0:
        clean, line_number, page = add_cleaning(cleaning, line_number, page)
        main_lines["cleaning"] = clean
    if "climate_outdoor_unit" in keys or "climate_indoor_unit" in keys:
        outdoor = house["climate_outdoor_unit"] if "climate_outdoor_unit" in keys else 0
        indoor = house["climate_indoor_unit"] if "climate_indoor_unit" in keys else 0
        if outdoor != 0 or indoor != 0:
            clima, line_number, page = add_clima(outdoor, indoor, line_number, page)
            for i, k in enumerate(clima.values(), start=1):
                main_lines[f"clima_{i}"] = k
    
    data = {"data":{
        "proj_description":{
            "project_id": Projects.gen_id(),
            "author": house["author"],
            "title": house["proj_title"],
            "address": house["address"],
            "n_pg": page if line_number != 1 else page - 1
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
                    "cable": "RZ1-K",
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
                        "cable": "H07Z1-K",
                        "pols": 2,
                        "seccion": "1,5mm"}}
                }
        }
        line_number, page = actualize_line_page(line_number, page)
        general_lines[i]["sub_lines"][1] = {
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
                    "description": f"Enchufes interiores {i+1}",
                    "cable": "H07Z1-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
        line_number, page = actualize_line_page(line_number, page)
        general_lines[i]["sub_lines"][2] = {
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
                    "description": f"Enchufes humedos {i+1}",
                    "cable": "H07Z1-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
        line_number, page = actualize_line_page(line_number, page)
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
                    "position_y": 760-100*(line_number),
                    "protec_type": "M",
                    "pols": 2,
                    "ampere": 10,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*(line_number),
                    "pols": 2,
                    "page": page,
                    "line_number": f"L{line_number+(7*(page-1))}",
                    "description": "Luz exterior",
                    "cable": "RZ1-K",
                    "pols": 2,
                    "seccion": "2,5mm"}
            }}
    }
    line_number, page = actualize_line_page(line_number, page)
    garden["sub_lines"][1] = {
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
                    "cable": "RZ1-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}

    line_number, page = actualize_line_page(line_number, page)
    return garden, line_number, page

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

def add_cleaning(cleaning: list, line_number, page):
    clean = {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": 2,
                "ampere": 40,
                "description": "30mA\nTipo AC",
                "page": page},
            "sub_lines":{}}
    for n, i in enumerate(cleaning):
        if i == "iron":
            name = "Plancha"
        elif i == "wash_machine":
            name = "Lavadora"
        elif i == "dryer":
            name = "Secadora"
        clean["sub_lines"][n] = {
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
                    "description": name,
                    "cable": "H07Z1-K",
                    "pols": 2,
                    "seccion": "2,5mm"}}
        line_number, page = actualize_line_page(line_number, page)
    return clean, line_number, page

def add_heating_system(system: str, line_number, page):
    heating_system = {"head_proteccion": {
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
                    "line_number": f"L{line_number}",
                    "description": f"{system}",
                    "cable": "RZ1-K",
                    "seccion": "2,5mm"}}
            }
    }
    if system == "Boiler":
        heating_system["sub_lines"][0]["line"]["description"] = "Caldera"
    if system == "Aerothermia":
        heating_system["head_proteccion"]["description"] = "30mA\nTipo SI"
        heating_system["sub_lines"][0]["line"]["description"] = "Aerotermia"
        heating_system["sub_lines"][0]["proteccion"]["ampere"] = 25
        heating_system["sub_lines"][0]["line"]["seccion"] = "4mm"
    if system == "Electric heater":
        heating_system["sub_lines"][0]["line"]["description"] = "Termo eléctrico"
        heating_system["sub_lines"][0]["proteccion"]["ampere"] = 20
        heating_system["sub_lines"][0]["line"]["seccion"] = "4mm"
    line_number, page = actualize_line_page(line_number, page)
    return heating_system, line_number, page

def add_clima(outdoor: int, indoor: int, line_number: int, page: int):
    clima_lines = {}
    for i in range(outdoor):
        clima_lines[i+1] = {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": 2,
                "ampere": 40,
                "description": "30mA\nTipo SI",
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
                    "line_number": f"L{line_number}",
                    "description": f"Unidad exterior {i + 1}",
                    "cable": "RZ1-K",
                    "seccion": "2,5mm"}}
            }
        }
        line_number, page = actualize_line_page(line_number, page)
    if outdoor == 0 or outdoor == 1:
        if outdoor == 0:
            clima_lines[1] = {"head_proteccion": {
                    "position_x": 139,
                    "position_y": 760-100*line_number,
                    "protec_type": "D",
                    "pols": 2,
                    "ampere": 40,
                    "description": "30mA\nTipo SI",
                    "page": page},
                "sub_lines":{}
                }
        if indoor >= 4:
            indoor1 = int(indoor/2) if indoor % 2 == 0 else int(indoor/2 + 1)
            indoor2 = indoor - indoor1
            for i in range(indoor1):
                unit_number = i + 1
                i = i +1 if clima_lines[1]["sub_lines"][i] else i
                clima_lines[1]["sub_lines"][i] = clima_final_line(unit_number, line_number, page)
                line_number, page = actualize_line_page(line_number, page)
            clima_lines[2] = {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": 2,
                "ampere": 40,
                "description": "30mA\nTipo SI",
                "page": page},
            "sub_lines":{}
            }
            for i in range(indoor2):
                unit_number = indoor1 + i + 1
                clima_lines[2]["sub_lines"][i] = clima_final_line(unit_number, line_number, page)
                line_number, page = actualize_line_page(line_number, page)
        else:
            for i in range(indoor):
                print(clima_lines)
                print("\n")
                unit_number = i + 1
                i = i + 1 if clima_lines[1]["sub_lines"][i] else i
                clima_lines[1]["sub_lines"][i] = clima_final_line(unit_number, line_number, page)
                line_number, page = actualize_line_page(line_number, page)
            print(clima_lines)
    elif len(clima_lines) == 2:
        indoor1 = int(indoor/2) if indoor % 2 == 0 else int(indoor/2 + 1)
        indoor2 = indoor - indoor1
        for i in range(indoor1):
            unit_number = i + 1
            clima_lines[1]["sub_lines"][i] = clima_final_line(unit_number, line_number, page)
            line_number, page = actualize_line_page(line_number, page)
        for i in range(indoor2):
            unit_number = indoor1 + i + 1
            clima_lines[2]["sub_lines"][i] = clima_final_line(unit_number, line_number, page)
            line_number, page = actualize_line_page(line_number, page)
    return clima_lines, line_number, page


def clima_final_line(unit_number, line_number, page):
    return {
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
            "line_number": f"L{line_number}",
            "description": f"Unidad interior {unit_number}",
            "cable": "RZ1-K",
            "seccion": "1,5mm"}}
            


def create_project(data: dict):
    proj_desc = data["proj_description"]
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

