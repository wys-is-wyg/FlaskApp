from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models.Account import Account

bp = Blueprint('account', __name__, url_prefix='', static_folder='../static')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    account = Account()
    
    if request.method == 'POST':
        error = None
        try:
            user = account.register(request)
        except Exception as err:
            error = err
        if error:
            flash(error)
        else:
            flash("Please login to get started!")
            return redirect(url_for('account.login'))

    return render_template('account/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    account = Account()
    
    if request.method == 'POST':
        error = None
        try:
            user = account.login(request)
        except Exception as err:
            error = err
        if error:
            flash(error)
        else:
            flash("Welcome back!")
            return redirect(url_for('account.profile'))

    return render_template('account/login.html')
    
@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    account = Account()

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
    
@bp.route('/logout')
def logout():
    account = Account()
    account.logout()
    return redirect(url_for('home.index'))
