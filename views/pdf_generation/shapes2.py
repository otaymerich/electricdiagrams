import fitz
from fitz import Point, Rect
from views.pdf_generation.shapes import text_line,create_frame, shape_singlephase_cable, shape_threephase_cable, text_frame,shape_diferencial, shape_horizontal_cable, shape_line, shape_magneto, shape_rectangle, add_textbox
from tkinter import filedialog
from views.pdf_generation.models import db, Proteccions, Projects, Lines
from views.elec.models import Users
from flask import session
import os.path
from PIL import Image
import io

'''
SCRIPT FOR COMPOSING THE PAGES OF THE PDF DOCUMENT
'''

def draw_cables (page_drawings: list, next_position_x = False, prev_position_x = False, multiple_next = False) -> list:
    '''Create horizontal line for multiple entrances of power'''
    entrance_line = list(filter(lambda protec: protec if protec.position_x==48  else None, page_drawings))
    entrance_line = sorted(list(map(lambda protec: protec.position_y, entrance_line)))
    cables_list = []
    if len(entrance_line) > 1:
        cables_list.extend(shape_horizontal_cable(99, entrance_line[0], entrance_line[-1]))
    '''Create general horizontal line'''
    general_line = list(filter(lambda protec: protec if protec.position_x==139  else None, page_drawings))
    general_line = sorted(list(map(lambda protec: protec.position_y, general_line)), reverse=True)
    if next_position_x == 139 or multiple_next:
        general_line.append(30)
    if prev_position_x:
        general_line.insert(0, 690)
    if len(general_line) > 1:
        cables_list.extend(shape_horizontal_cable(119, general_line[0], general_line[-1]))
    '''Create horizontal sub_lines'''
    sub_lines = list(filter(lambda protec: protec if protec.position_x==220 else None, page_drawings))
    sub_lines = sorted(list(map(lambda protec: protec.position_y, sub_lines)), reverse=True)
    if next_position_x == 220 or multiple_next:
        sub_lines.append(30)
    if prev_position_x == 220:
        sub_lines.insert(0, 690)
    for protec_y in sub_lines:
        if protec_y - 100 in sub_lines and protec_y - 100 not in general_line:
            cables_list.extend(shape_horizontal_cable(200, protec_y, protec_y-100))
        elif protec_y == 690:
            cables_list.extend(shape_horizontal_cable(200, 660, 690))
        elif protec_y == 30:
            cables_list.extend(shape_horizontal_cable(200, 60, 30))
    return cables_list

def draw_page(project: object, page: int) -> tuple:
    '''
    Drawing proteccions
    '''
    protec_drawings = list(Proteccions.query.filter_by(project_id=project.id, page=page).all())
    next_protec_y = Proteccions.query.filter_by(project_id=project.id, page=page+1, position_y=660).first()
    next_protec_x = Proteccions.query.filter_by(project_id=project.id, page=page+1, position_x=139).first()
    if next_protec_x and next_protec_y and next_protec_x != next_protec_y:
        multiple_next = True
        next_protec = next_protec_y
    elif next_protec_y:
        next_protec = next_protec_y
        multiple_next = False
    else:
        next_protec = next_protec_x
        multiple_next = False
    if page > 1:
        prev_protec = Proteccions.query.filter_by(project_id=project.id, page=page, position_y=660).first()
    else:
        prev_protec = None
    draw_list = create_frame()
    if next_protec and prev_protec:
        draw_list.extend(draw_cables(protec_drawings, next_protec.position_x, prev_protec.position_x, multiple_next))
    elif next_protec and prev_protec == None:
        draw_list.extend(draw_cables(protec_drawings, next_protec.position_x, False , multiple_next))
    elif next_protec == None and prev_protec:
        draw_list.extend(draw_cables(protec_drawings, False, prev_protec.position_x, multiple_next))
    else:
        draw_list.extend(draw_cables(protec_drawings))
    text_list = text_frame(project.title, project.author, page)

    for protec in protec_drawings:
        x = protec.position_x
        y = protec.position_y
        if protec.protec_type == "M":
            if protec.description == "Solar":
                draw_list.extend(shape_magneto(x,y, True))
            else:
                draw_list.extend(shape_magneto(x,y))
        elif protec.protec_type == "D":
            draw_list.extend(shape_diferencial(x,y))
        text = f"{protec.pols}P\n{protec.ampere}A\n{protec.description}"
        if protec.description == "Solar":
            text = f"Placas solares\n\n{protec.pols}P\n{protec.ampere}A\nC"
            x = x-20
        text_list.extend([(Point(x+10, y-10), text, (0,0,1))])
    '''
    Drawing lines
    '''
    line_drawings = list(Lines.query.filter_by(project_id=project.id, page=page).all())
    for line in line_drawings:
        if line.pols == 2:
            draw_list.extend(shape_singlephase_cable(line.position_y))
        elif line.pols == 4:
            draw_list.extend(shape_threephase_cable(line.position_y))
    for line in line_drawings:
        text_list.extend(text_line(line))
    return draw_list, text_list

def create_pdf(project: object):
    '''
    open document
    '''
    user = Users.query.filter_by(id=session.get("id")).first()
    doc = fitz.open()
    for page in range(project.n_pg):
        page = page + 1
        outpage = doc.new_page(width=595, height=842)
        shape = outpage.new_shape()
        '''
        generates the lists to create the drawings and the texts from the db
        '''
        draw_list, text_list = draw_page(project, page)
        '''
        draw the entries from draw_list
        '''
        for path in draw_list:
            for item in path["items"]:  # these are the draw commands
                if item[0] == "l":  # line   
                    shape.draw_line(item[1], item[2])
                elif item[0] == "re":  # rectangle
                    shape.draw_rect(item[1])
                elif item[0] == "qu":  # quad
                    shape.draw_quad(item[1])
                elif item[0] == "c":  # curve
                    shape.draw_bezier(item[1], item[2], item[3], item[4])
                elif item[0] == "circle":
                    shape.draw_circle(item[1],item[2])
                else:
                    raise ValueError("unhandled drawing", item)
            shape.finish(
                fill=path["fill"],  # fill color
                color=path["color"],  # line color
                dashes=path["dashes"],  # line dashing
                even_odd=path.get("even_odd", True),  # control color of overlaps
                closePath=path["closePath"],  # whether to connect last and first point
                lineJoin=path["lineJoin"],  # how line joins should look like
                lineCap=max(path["lineCap"]),  # how line ends should look like
                width=path["width"],  # line width
                stroke_opacity=path.get("stroke_opacity", 1),  # same value for both
                fill_opacity=path.get("fill_opacity", 1),  # opacity parameters
                )
            shape.commit()
        '''
        rotate document
        '''
        for pg in doc: pg.set_rotation(90)
        '''
        insert texts
        '''
        for textbox in text_list:
            if type(textbox[0]) == Point:
                outpage.insert_text(textbox[0], textbox[1], fontsize=9.5, fontname='helv', fontfile=None, color=textbox[2], fill=None, render_mode=0, border_width=1, rotate=90, morph=None, stroke_opacity=1, fill_opacity=1, overlay=True, oc=0)
            elif type(textbox[0]) == Rect:
                outpage.insert_textbox(textbox[0], textbox[1], fontsize=9.5, fontname='helv', fontfile=None, color=textbox[2], fill=None, render_mode=0, border_width=1, encoding='utf8', expandtabs=8, align=1, rotate=90, morph=None, stroke_opacity=1, fill_opacity=1, oc=0, overlay=True)
    '''
    insert company logo
    #'''
    if os.path.exists(f"static/logos/{user.id}_logo.png"):
        rect = fitz.Rect(537,612,583,830)
        img = open(f"static/logos/{user.id}_logo.png", "rb").read()
        for page in doc:
            page.insert_image(rect, stream=img, xref=0, rotate=90, keep_proportion=True) #It dosn't keep the proportion this sucker, check

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("pdf file","*.pdf")])
    if file_path:
        doc.save(file_path)
    doc.close()
    print(fitz.__doc__)


if __name__ == "__main__":
    pass