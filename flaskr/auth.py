import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def sanitize_input(user_input):
    blacklisted_words = ['union','select','drop','alter']
    return any(word in user_input.lower() for word in blacklisted_words)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'

        if error is None and sanitize_input(username) and sanitize_input(password):
            try:
                db.execute(
                    f"INSERT INTO user (username,password) VALUES ('{username}','{password}')",
                    #(username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f'error occured'
            else:
                return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user == 'admin' and user['password']==password:
            return render_template('auth/flag.html')
        if user is None:
            error = 'Incorrect username.'
        elif not user['password']==password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
