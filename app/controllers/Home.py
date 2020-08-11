from app.models.Image import Image
from flask import Blueprint, render_template, flash, session
from flask import current_app as flask_app

bp = Blueprint('home', __name__, url_prefix='', static_folder='../static')

# Load the index page
@bp.route('/')
def index():

    error = None
    latest_images = []
    try:
        image_model = Image()
        latest_images = image_model.get_latest_images()
    except Exception as err:
        error = err
    if error:
        flash(error)

    return render_template('home.html', latest_images=latest_images)

@bp.errorhandler(404)
def error404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404