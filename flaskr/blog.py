from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'select post.id, title, body, created_at, author_id, username from post join user on post.author_id = user.id order by created_at desc'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'title required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'insert into post (title,body,author_id) values (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'select post.id, title, body, created_at, author_id, username from post join user on post.author_id = user.id where post.id = ?', (
            id,)
    ).fetchone()

    if post is None:
        abort(404, f'post with id {id} is not found')

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'update post set title = ?, body = ? where id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(
        'delete from post where id = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))

'''
def search_post(post_name):

    return
'''