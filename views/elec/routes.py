from flask import Blueprint, render_template, request, session, url_for, redirect

elec = Blueprint("elec", __name__)