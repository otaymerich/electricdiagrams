from views.pdf_generation.models import db, Projects, Lines, Proteccions

'''
SCRIPT FOR GENERATING THE DATA FOR EACH ELECTRIC SCHEME
'''


def actualize_line_page(line_number: int, page: int) -> tuple: #ASSIGNS THE NEXT LINE NUMBER AND CHECKS IF THERE IS A PAGE JUMP
    if line_number < 7:
            line_number += 1
    else:
        line_number = 1
        page = page +1
    return line_number, page

def organize_house(house: dict) -> str: #GENERATES THE DICT WITH JSON FORMAT THATS GONA BE USED TO DRAW THE PDF AND SAVES THE DATA IN THE PDF.DB
    print(house)
    line_number = 1
    page = 1
    main_lines = {}
    keys = house.keys()
    if "pool" in keys:
        pool, line_number, page = add_pool(line_number, page)
        main_lines["pool"] = pool
    if "garden" in keys:
        garden, line_number, page = add_garden(line_number, page)
        main_lines["garden"] = garden
    heating_system, line_number, page = add_heating_system(house["heating_system"], line_number, page)
    main_lines["heating_system"] = heating_system
    general, line_number, page = add_generallines(house["floors"], house["m2"], line_number, page)
    for i, k in enumerate(general.values(), start=1):
        main_lines[f"general_{i}"] = k
    cleaning = list(filter(lambda key: key if key == "wash_machine" or key == "iron" or key == "dryer" else None, keys))
    kitchen1 = list(filter(lambda element: element == "fridge" or element == "freezer", keys))
    if len(kitchen1) > 0:
        kitchen_lines1, line_number, page = add_kitchen_1(kitchen1, line_number, page)
        main_lines["kitchen_1"] = kitchen_lines1
    kitchen2 = list(filter(lambda element: element == "oven" or element == "dishwasher", keys))
    if len(kitchen2) > 0:
        kitchen_lines2, line_number, page = add_kitchen_2(kitchen2, line_number, page)
        main_lines["kitchen_2"] = kitchen_lines2
    if "vitro_hub" in keys:
        vitro, line_number, page = add_vitro(line_number, page)
        main_lines["vitro"] = vitro
    if len(cleaning) > 0:
        clean, line_number, page = add_cleaning(cleaning, line_number, page)
        main_lines["cleaning"] = clean
    if "climate_outdoor_unit" in keys or "climate_indoor_unit" in keys:
        outdoor = house["climate_outdoor_unit"] if house["climate_outdoor_unit"]  else 0
        indoor = house["climate_indoor_unit"] if house["climate_indoor_unit"] else 0
        if outdoor != 0 or indoor != 0:
            clima, line_number, page = add_clima(outdoor, indoor, line_number, page)
            for i, k in enumerate(clima.values(), start=1):
                main_lines[f"clima_{i}"] = k
    extras = list(filter(lambda element: element == "alarm" or element == "electronics" or element == "domotics", keys))
    if len(extras) > 0:
        extra, line_number, page = add_extras(extras, line_number, page)
        main_lines["extras"] = extra
    if "elec_car" in keys:
        car, line_number, page = add_car(line_number, page)
        main_lines["car"] = car
    data = {"data":{
        "proj_description":{
            "project_id": Projects.gen_id(),
            "house_id": house["id"],
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

def add_entrance(data: dict) -> dict:
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

def add_solar() -> dict:
    return {"position_x": 48,
        "position_y": 560,
        "protec_type": "M",
        "pols": 2,
        "ampere": 20,
        "description": "Solar",
        "page": 1}

def add_pool(line_number: int, page: int) -> tuple:
    pool = create_head_proteccion(2, "300mA\nTipo AC-S", line_number, page)
    pool["sub_lines"].update(create_sub_line(0, 2, 20, "Sbq. Piscina", "RZ1-K", "4mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    return pool, line_number, page

def add_generallines(floors: int, m2: int, line_number: int, page: int) -> tuple:
    if floors == 1 and m2 > 300:
        n = 2
    else:
        n = floors
    general_lines = {}
    for i in range(n):
        general_lines[i] = create_head_proteccion(2, "30mA\nTipo AC", line_number, page)
        general_lines[i]["sub_lines"].update(create_sub_line(0, 2, 10, f"Luces interiores {i+1}", "H07Z1-K", "1,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
        general_lines[i]["sub_lines"].update(create_sub_line(1, 2, 16, f"Enchufes interiores {i+1}", "H07Z1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
        general_lines[i]["sub_lines"].update(create_sub_line(2, 2, 16, f"Enchufes humedos {i+1}", "H07Z1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    return general_lines, line_number, page

def add_garden(line_number: int, page: int) -> tuple:
    garden = create_head_proteccion(2, "30mA\nTipo AC", line_number, page)
    garden["sub_lines"].update(create_sub_line(0, 2, 10, "Luz exterior", "RZ1-K", "1,5mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    garden["sub_lines"].update(create_sub_line(1, 2, 16, "Enchufes exteriores", "RZ1-K", "2,5mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    return garden, line_number, page


def add_cleaning(cleaning: list, line_number: int, page: int) -> tuple:
    clean = create_head_proteccion(2, "30mA\nTipo AC", line_number, page)
    for n, i in enumerate(cleaning):
        if i == "iron":
            name = "Plancha"
        elif i == "wash_machine":
            name = "Lavadora"
        elif i == "dryer":
            name = "Secadora"
        clean["sub_lines"].update(create_sub_line(n, 2, 16, name, "H07Z1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    return clean, line_number, page

def add_heating_system(system: str, line_number: int, page: int) -> tuple:
    heating_system = create_head_proteccion(2, "30mA\nTipo AC", line_number, page)
    if system == "Boiler":
        heating_system["sub_lines"].update(create_sub_line(0, 2, 16, "Caldera", "H07Z1-K", "2,5mm", line_number, page))
    elif system == "Aerothermia":
        heating_system["sub_lines"].update(create_sub_line(0, 2, 25, "Aerot??rmia", "H07Z1-K", "4mm", line_number, page))
        heating_system["head_proteccion"]["description"] = "30mA\nTipo SI"
    elif system == "Electric heater":
        heating_system["sub_lines"].update(create_sub_line(0, 2, 20, "Termo el??ctrico", "H07Z1-K", "4mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    return heating_system, line_number, page

def add_clima(outdoor: int, indoor: int, line_number: int, page: int) -> tuple:
    clima_lines = {}
    if outdoor != 0:
        clima_lines[1] = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
        clima_lines[1]["sub_lines"].update(create_sub_line(0, 2, 16, "Unidad exterior 1", "RZ1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    if outdoor == 0 or outdoor == 1:
        if outdoor == 0:
            clima_lines[1] = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
        if indoor >= 4:
            indoor1 = int(indoor/2) if indoor % 2 == 0 else int(indoor/2 + 1)
            indoor2 = indoor - indoor1
            for i in range(indoor1):
                unit_number = i + 1
                i = i +1 if i in clima_lines[1]["sub_lines"].keys() else i
                clima_lines[1]["sub_lines"].update(create_sub_line(i, 2, 16, f"Unidad interior {unit_number}", "RZ1-K", "2,5mm", line_number, page))
                line_number, page = actualize_line_page(line_number, page)
            clima_lines[2] = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
            for i in range(indoor2):
                unit_number = indoor1 + i + 1
                clima_lines[2]["sub_lines"].update(create_sub_line(i, 2, 16, f"Unidad interior {unit_number}", "RZ1-K", "2,5mm", line_number, page))
                line_number, page = actualize_line_page(line_number, page)
        else:
            for i in range(indoor):
                unit_number = i + 1
                i = i +1 if i in clima_lines[1]["sub_lines"].keys() else i
                clima_lines[1]["sub_lines"].update(create_sub_line(i, 2, 16, f"Unidad interior {unit_number}", "RZ1-K", "2,5mm", line_number, page))
                line_number, page = actualize_line_page(line_number, page)
    elif outdoor == 2:
        indoor1 = int(indoor/2) if indoor % 2 == 0 else int(indoor/2 + 1)
        indoor2 = indoor - indoor1
        for i in range(indoor1):
            unit_number = i + 1
            clima_lines[1]["sub_lines"].update(create_sub_line(i+1, 2, 16, f"Unidad interior {unit_number}", "RZ1-K", "2,5mm", line_number, page))
            line_number, page = actualize_line_page(line_number, page)
        clima_lines[2] = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
        clima_lines[2]["sub_lines"].update(create_sub_line(0, 2, 16, "Unidad exterior 2", "RZ1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
        for i in range(indoor2):
            unit_number = indoor1 + i + 1
            clima_lines[2]["sub_lines"].update(create_sub_line(i+1, 2, 16, f"Unidad interior {unit_number}", "RZ1-K", "2,5mm", line_number, page))
            line_number, page = actualize_line_page(line_number, page)
    return clima_lines, line_number, page

def add_kitchen_1(elements: list, line_number: int, page: int) -> tuple:
    kitchen = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
    for n, element in enumerate(elements):
        if element == "fridge":
            name = "Nevera"
        elif element == "freezer":
            name = "Congelador"
        kitchen["sub_lines"].update(create_sub_line(n, 2, 16, name, "H07Z1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    return kitchen, line_number, page

def add_kitchen_2(elements: list, line_number:int, page: int) -> tuple:
    kitchen = create_head_proteccion(2, "30mA\nTipo AC", line_number, page)
    for n, element in enumerate(elements):
        if element == "oven":
            kitchen["sub_lines"].update(create_sub_line(n, 2, 20, "Horno", "H07Z1-K", "4mm", line_number, page))
        elif element == "dishwasher":
            kitchen["sub_lines"].update(create_sub_line(n, 2, 16, "Lavaplatos", "H07Z1-K", "2,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    return kitchen, line_number, page
        
def add_vitro(line_number: int, page: int) -> tuple:
    vitro = create_head_proteccion(4, "30mA\nTipo SI", line_number, page)
    vitro["sub_lines"].update(create_sub_line(0, 4, 16, "Vitrocer??mica", "RZ1-K", "2,5mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    return vitro, line_number, page

def add_extras(elements: list, line_number: int, page: int) -> tuple:
    extra = create_head_proteccion(2, "30mA\nTipo SI", line_number, page)
    for n, element in enumerate(elements):
        if element == "alarm":
            extra["sub_lines"].update(create_sub_line(n, 2, 10, "Alarma", "H07Z1-K", "1,5mm", line_number, page))
        elif element == "electronics":
            extra["sub_lines"].update(create_sub_line(n, 2, 10, "Electr??nica", "H07Z1-K", "1,5mm", line_number, page))
        elif element == "domotics":
            extra["sub_lines"].update(create_sub_line(n, 2, 10, "Dom??tica", "H07Z1-K", "1,5mm", line_number, page))
        line_number, page = actualize_line_page(line_number, page)
    return extra, line_number, page

def add_car(line_number: int, page: int) -> tuple:
    car =   create_head_proteccion(4, "30mA\nTipo SI", line_number, page)
    car["sub_lines"].update(create_sub_line(0, 4, 20, "Carg. coche el??ctrico", "RZ1-K", "4mm", line_number, page))
    line_number, page = actualize_line_page(line_number, page)
    return car, line_number, page

def create_head_proteccion(pols: int, description: str, line_number: int, page: int) -> dict:
    head_proteccion =  {"head_proteccion": {
                "position_x": 139,
                "position_y": 760-100*line_number,
                "protec_type": "D",
                "pols": pols,
                "ampere": 40,
                "description": description,
                "page": page},
            "sub_lines":{}
    }
    return head_proteccion

def create_sub_line(n_subline: int, pols: int, ampere: int, line_description: str, cable: str, seccion: str, line_number: int, page: int) -> dict:
    return {n_subline:{
                "proteccion":{
                    "position_x": 220,
                    "position_y": 760-100*line_number,
                    "protec_type": "M",
                    "pols": pols,
                    "ampere": ampere,
                    "description": "C",
                    "page": page},
                "line":{
                    "position_y": 760-100*line_number,
                    "pols": pols,
                    "page": page,
                    "line_number": f"L{line_number+(7*(page-1))}",
                    "description": line_description,
                    "cable": cable,
                    "seccion": seccion}}
    }

def create_project(data: dict) -> str: 
    proj_desc = data["proj_description"]
    new_project = Projects(proj_desc["project_id"],
                        proj_desc["house_id"],
                        proj_desc["author"],
                        proj_desc["title"],
                        proj_desc["address"],
                        proj_desc["n_pg"])
    db.session.add(new_project)
    db.session.commit()
    for entrance in data["power_entrance"].values():
        create_proteccion(entrance, proj_desc["project_id"])
    create_lines(data["lines"], proj_desc["project_id"])
    return "Success" #Useless confirmation of everything went alright

def create_lines(lines: dict, proj_id: str) -> str:
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
    return "Success" #Useless confirmation of everything went alright

def create_proteccion(proteccion: dict, proj_id: str) -> str:
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
    return "Success" #Useless confirmation of everything went alright

