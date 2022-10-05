from fitz import Point, Rect
import datetime

level_1 = 48
level_2 = 139
level_3 = 220
author = "Ot Aymerich Alemany"

def shape_singlephase_cable(y: float) -> list:
    singlephase = [{'items': [], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    items = [('l', Point(290, y), Point(406, y)), #cable
            ('circle', Point(400, y), 4), #borne
            ('l', Point(403.5, y+2), Point(396.5, y-2)),
            ('l', Point(385, y+10), Point(377, y-10)),#marca monofasic
            ('l', Point(388, y+10), Point(380, y-10))]
    singlephase[0]["items"] = items
    return singlephase

def shape_threephase_cable(y: float) -> list:
    threephase = [{'items': [], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    items = [('l', Point(290, y), Point(436, y)),#cable
            ('circle', Point(490, y), 4),#borne
            ('l', Point(403.5, y+2), Point(396.5, y-2)),
            ('l', Point(385, y+10), Point(377, y-10)),#marca cable trifasic
            ('l', Point(388, y+10), Point(380, y-10)),
            ('l', Point(391, y+10), Point(383, y-10)),
            ('l', Point(394, y+10), Point(386, y-10))]
    threephase[0]["items"] = items
    return threephase

def shape_magneto (x: float, y: float) -> list:
    magneto = [{'items': [], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    items = [('l', Point(x-20, y), Point(x+19, y)),
            ('l', Point(x+19, y+3), Point(x+19, y-3)),
            ('l', Point(x+21, y+6), Point(x+39, y)),
            ('l', Point(x+39, y), Point(x+71, y)),
            ('l', Point(x+17, y+3), Point(x+11, y-3)),
            ('l', Point(x+11, y+3), Point(x+17, y-3))]
    magneto[0]["items"] = items
    return magneto

def shape_diferencial (x: float, y: float) -> list:
    diferencial = [{'items': [], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    items = [('l', Point(x-20, y), Point(x+17, y)),
            ('circle', Point(x+19, y), 2),
            ('l', Point(x+21, y+6), Point(x+39, y)),
            ('l', Point(x+16, y-3), Point(x+16, y+3)),
            ('l', Point(x+39, y), Point(x+71, y))]
    diferencial[0]["items"] = items
    return diferencial

def shape_horizontal_cable (x: float, y: float, n: int) -> list:
    cable = [{'items': [], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    items = [('l', Point(x, y), Point(x, y-100*n))]
    cable[0]["items"] = items
    return cable

def add_textbox(x: float,y: float,text: str, colour: str) -> list:
    return [(Point(x,y), text, colour)]
    
def shape_rectangle(x1: int, y1: int, x2: int, y2: int) -> list:
    rectangle = [{'items': [("re", Rect(Point(x1,y1),Point(x2, y2)))], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    return rectangle

def shape_line(x1: int, y1: int, x2: int, y2: int) -> list:
    line = [{'items': [('l', Point(x1, y1), Point(x2, y2))], 'stroke_opacity': 1.0, 'color': (0.0, 0.0, 0.0), 'width': 0.0, 'lineCap': (0, 0, 0), 'lineJoin': 0.0, 'dashes': '[] 0', 'closePath': False, 'fill': None, 'fill_opacity': 1, 'even_odd': True}]
    return line

def create_frame() -> list:
    draw_list = shape_rectangle(10,10,585,832)
    draw_list.extend(shape_line(435, 110, 585, 110))
    draw_list.extend(shape_line(435, 210, 535, 210))
    draw_list.extend(shape_line(435, 310, 535, 310))
    draw_list.extend(shape_line(435, 410, 535, 410))
    draw_list.extend(shape_line(435, 510, 535, 510))
    draw_list.extend(shape_line(435, 610, 585, 610))
    draw_list.extend(shape_line(435, 710, 535, 710))
    draw_list.extend(shape_line(435,10,435,832))
    draw_list.extend(shape_line(455,10,455,832))
    draw_list.extend(shape_line(495,10,495,832))
    draw_list.extend(shape_line(515,10,515,832))
    draw_list.extend(shape_line(535,10,535,832))
    return draw_list

def text_frame(title) -> list:
    text_list = add_textbox(448, 827, "ID Línea", (0,0,0))
    text_list.extend(add_textbox(478, 827, "Descripción", (0,0,0)))
    text_list.extend(add_textbox(508, 827, "Tipo de cable", (0,0,0)))
    text_list.extend(add_textbox(528, 827, "Sección", (0,0,0)))
    text_list.extend(add_textbox(578, 50, "Pg. 1", (0,0,0)))
    text_list.append((Rect(Point(540,110),Point(573, 610)), title, (0,0,0)))
    text_list.extend(add_textbox(568, 600, f"Autor: {author}", (0,0,0)))
    text_list.extend(add_textbox(580, 600, data(), (0,0,0)))
    return text_list

def data():
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    date = datetime.datetime.now()
    final_date = f'''{days[int(date.strftime("%w"))]} {date.strftime("%d")} de {months[int(date.strftime("%m"))-1]}, {date.strftime("%Y")}'''
    return final_date

def text_line(line: dict) -> list:
    y = 710-100*(int(line["posicion"])-1)
    text_list = [(Rect(Point(435, y-100),Point(455, y)), line["lineid"], (0,0,0))]
    text_list.append((Rect(Point(455, y-100),Point(495, y)), line["description"], (0,0,0)))
    text_list.append((Rect(Point(495, y-100),Point(515, y)), line["cabletype"], (0,0,0)))
    text_list.append((Rect(Point(515, y-100),Point(535, y)), f'''{line["pols"]}x{line["seccion"]}''', (0,0,0)))
    return text_list

def nex_page(level):
    pass


if __name__ == "__main__":
    pass
