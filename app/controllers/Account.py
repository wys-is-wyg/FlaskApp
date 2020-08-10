from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask import current_app as flask_app
from app.models.Account import Account

bp = Blueprint('account', __name__, url_prefix='', static_folder='../static')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    
    if request.method == 'POST':
        error = None
        try:
            account = Account()
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
    
    if request.method == 'POST':
        error = None
        try:
            account = Account()
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

    if request.method == 'POST':
        error = None
        try:
            account = Account()
            user = account.update(request)
        except Exception as err:
            error = err
        if error:
            flash(error)

    return render_template('account/profile.html')
    
@bp.route('/logout')
def logout():
    account = Account()
    account.logout()
    return redirect(url_for('home.index'))
