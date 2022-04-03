from flask import Flask, render_template
from flask import Blueprint
from database import get_db


contact_api = Blueprint('contact_api', __name__)


@contact_api.route("/contact-us")
def initialiseContactUs():
    return render_template('contact.html')
