import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app as flask_app
from app import ARA_SITE_ROOT

class Upload():
    
    UPLOAD_FOLDER =  'app/static/uploads/'

    def __init__(self):
        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}

    def upload(self, file, filename):

        if self.allowed_file(file.filename):
            file.save(os.path.join(ARA_SITE_ROOT, UPLOAD_FOLDER, filename))
            flask_app.logger.info(os.path.join(ARA_SITE_ROOT, UPLOAD_FOLDER, filename))
        else:
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions