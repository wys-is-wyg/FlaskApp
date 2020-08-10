from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app

class Account():

    def __init__(self):
        self.user = User()

    def register(self, request):
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        error = None
        if not email:
            error = 'An email is required.'
        elif not password:
            error = 'Password is required.'
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        elif not password_confirm:
            error = 'Password confirmation is required.'
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                database = Database()
                user_auth = database.register(email, password)
            except Exception as err:
                error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def login(self, request):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            error = None
            if not email:
                error = 'An email is required.'
            elif not password:
                error = 'Password is required.'
            else:
                try:
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def update(self, request):
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            if not first_name:
                error = 'A first name is required.'
            elif not last_name:
                error = 'A last name is required.'
            else:
                if 'file' in request.files:
                    file = request.files['file']
                    uploader = Upload()
                    avatar = uploader.upload(file, session['user']['localId'])
                    flask_app.logger.info(avatar)
                try:
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                except Exception as err:
                    error = err
            if error:
                flash(error)

        return render_template('account/profile.html')
        
    def logout(self):
        self.user.unset_user()
