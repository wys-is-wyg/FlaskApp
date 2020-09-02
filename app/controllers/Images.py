from app.models.Image import Image
from flask import Blueprint, render_template, request, flash, session
from flask import current_app as flask_app

bp = Blueprint('images', __name__, url_prefix='/images', static_folder='../static')
   
@bp.route('/', methods=('GET', 'POST'))
def images():

    error = None
    images = []
    try:
        image_model = Image()
        images = image_model.get_user_images()
    except Exception as err:
        error = err
    if error:
        flash(str(error))

    return render_template('images/images.html', images=images)
   
@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    
    if request.method == 'POST':
        error = None
        try:
            image_model = Image()
            image = image_model.upload(request)
            flash("Your Image has been uploaded")
        except Exception as err:
            error = err
        if error:
            flash(str(error))

    return render_template('images/upload.html')
    
    
@bp.route('/category')
def category():
    
    if request.method == 'GET':
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
            flash(str(error))
        else:
            flash("Your file has been uploaded!")

    return render_template('images/upload.html')