from app.classes.Database import Database
from flask import Blueprint, render_template, request, flash
from werkzeug.utils import secure_filename

bp = Blueprint('images', __name__, url_prefix='/images', static_folder='../static')

# Load the index page
@bp.route('/')
def images():
    return render_template('images/images.html')

    
# Load the index page
@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    
    if request.method == 'POST':
        error = None
        # check if the post request has the file part
        if 'file' not in request.files:
            error = 'No selected file.'
        else:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                error = 'No selected file.'
            else :
                try:
                    database = Database()
                    result = database.upload(file)
                except Exception as err:
                    error = err

        if error:
            flash(error)
        else:
            flash("Your file has been uploaded!")

    return render_template('images/upload.html')