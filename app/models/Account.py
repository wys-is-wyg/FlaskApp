from app.classes.Database import Database
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
                user = database.register(email, password)
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
                    user_auth = database.login(email, password)
                    # TODO Remove for production
                    flask_app.logger.info(user_auth)
                    self.user.set_user(user_auth)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def profile(self, request):
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
                    user_auth = database.update_user(email, password)
                except Exception as err:
                    error = err
            if error:
                flash(error)
            else:
                return redirect(url_for('index'))

        return render_template('account/profile.html')
        
    def logout(self):
        self.user.unset_user()
