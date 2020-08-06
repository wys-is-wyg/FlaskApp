import os
import tempfile
import pyrebase
import requests
import json
from app import ARA_SITE_ROOT

class Database():

    UPLOAD_FOLDER = 'app/uploads'

    def __init__(self):
        firebase_config_file = os.path.join(ARA_SITE_ROOT, 'firebase.json')
        firebase_config = json.load(open(firebase_config_file))
        
        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.readable_errors = {
            "INVALID_PASSWORD": "This is an invalid password",
            "EMAIL_NOT_FOUND": "This email has not been registered",
            "EMAIL_EXISTS": "This email already exists. Try logging in instead.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts, please try again later",
            "USER_DISABLED": "This account has been disabled by an administrator.",
        }
        
    def register(self, email, password):
        try:
            user_auth = self.auth.create_user_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as error:
            readable_error = self.get_readable_error(error)
            raise Exception(readable_error)

    def login(self, email, password):
        try:
            user_auth = self.auth.sign_in_with_email_and_password(email, password)
            return user_auth
        except requests.exceptions.HTTPError as error:
            readable_error = self.get_readable_error(error)
            raise Exception(readable_error)

    def get_latest_images(self):
        storage = self.firebase.storage()
        files = storage.list_files()
        return files

    def upload(self, file):

        if self.allowed_file(file.filename):
            try:
                user = User()
                user_id_token = ARA_USER.get_user_id_token()
                user_id = ARA_USER.get_user_id()
                temp = tempfile.NamedTemporaryFile(prefix=user_id, delete=False)
                file.save(temp.name)
                filename, file_extension = os.path.splitext(file.filename)
                new_name = temp.name.split("\\")[-1] + file_extension
                storage = self.firebase.storage()
                result = storage.child(new_name).put(temp.name, user_id_token)
                return result
            except requests.exceptions.HTTPError as error:
                readable_error = self.get_readable_error(error)
                raise Exception(readable_error)
        else:
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions

    def get_readable_error(self, error):
        error_json = error.args[1]
        error_messsage = json.loads(error_json)['error']['message']
        if error_messsage in self.readable_errors.keys(): 
            return self.readable_errors[error_messsage]
        else: 
            return "There was a problem with your request."