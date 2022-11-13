from app import app
from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)

from .models import User


@app.errorhandler(404)
def error_404(error):
    context = {
        'error': error.description,
        'error_code': error.code,
        'error_name': error.name
    }
    return render_template('error_page.html', **context), error.code


@app.route('/')
def index():
    menu = ['test1', 'test2', 'test3']
    context = {
        'title': 'hello world',
        'menu': menu,
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    test_password = '12345'
    test_email = 'admin@admin.admin'
    if request.method == 'POST':
        if request.form.get('password') != '12345':
            flash(request.form.get('email'), category='email')
            flash('Неверный пароль', category='error')
    context = {}
    if 'email' in session:
        return redirect(url_for('index'), 301)
    elif (
        request.method == 'POST'
        and request.form.get('email') == test_email
        and request.form.get('password') == test_password
    ):
        session['email'] = test_email
        return redirect(url_for('index'), 301)
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'), 301)


@app.route('/job/<category>/<int:id>')
def vacancy_detail(category, id):
    check_email = session.get('email')
    if not check_email:
        abort(401)
    context = {
        'vacancy': id,
        'category': category
    }
    return render_template('vacancy_detail.html', **context)
