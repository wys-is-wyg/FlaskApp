import os
import tempfile
import pyrebase
import requests
import json
from flask import current_app as flask_app
from app import ARA_SITE_ROOT

class Database():

    def __init__(self):
        firebase_config_file = os.path.join(ARA_SITE_ROOT, 'firebase.json')
        firebase_config = json.load(open(firebase_config_file))
        firebase_config["serviceAccount"] = os.path.join(ARA_SITE_ROOT, 'firebase.admin.json')
        
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
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
            data = {
                "localId": user_auth['localId'],
                "email": email,
                "first_name": "",
                "last_name": "",
                "avatar": ""
            }
            self.db.child("users").child(user_auth['localId']).set(data)
            return user_auth
        except requests.exceptions.HTTPError as error:
            flask_app.logger.info(error)
            readable_error = self.get_readable_error(error)
            raise Exception(readable_error)

    def login(self, email, password):
        try:
            user_auth = self.auth.sign_in_with_email_and_password(email, password)
            user = self.db.child("users").child(user_auth['localId']).get().val()
            return user
        except requests.exceptions.HTTPError as error:
            flask_app.logger.info(error)
            readable_error = self.get_readable_error(error)
            raise Exception(readable_error)

    def update_user(self, user_data):
        try:
            self.db.child("users").child(user_data['localId']).update(user_data)
            return
        except requests.exceptions.HTTPError as error:
            flask_app.logger.info(error)
            readable_error = self.get_readable_error(error)
            raise Exception(readable_error)

    def get_readable_error(self, error):
        error_json = error.args[1]
        error_messsage = json.loads(error_json)['error']['message']
        if error_messsage in self.readable_errors.keys(): 
            return self.readable_errors[error_messsage]
        else: 
            return "There was a problem with your request."