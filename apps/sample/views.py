"""
import uuid
from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from apps.main import db
from apps.sample.forms import SampleForm
from apps.sample.models import Samples
from apps.resource.models import ResourceGroups

sample = Blueprint(
    "sample",
    __name__,
    template_folder="templates",
    static_folder = "static"
)

@sample.route("/", methods=["GET"])
@login_required
def index():
    return render_template("sample/index.html")
"""