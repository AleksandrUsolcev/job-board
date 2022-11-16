from app import app, db
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from slugify import slugify
from werkzeug.urls import url_parse

from .forms import CategoryForm, LoginForm
from .models import Category, User


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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверная пара почты/пароля', category='user')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    if request.form.get('email'):
        flash(request.form.get('email'), category='email')
    context = {'form': form}
    return render_template('login.html', **context)


@app.route('/user_logout')
def logout():
    logout_user()
    return redirect(url_for('index'), 301)


@app.route('/job/add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        slug = slugify(form.data.get('name'))
        category = Category(
            slug=slug,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('category_detail', category=slug), 301)
    context = {'form': form}
    return render_template('board/category_add.html', **context)


@app.route('/job/<category>')
def category_detail(category):
    category = Category.query.filter_by(slug=category).first()
    context = {
        'category': category
    }
    return render_template('board/category_detail.html', **context)


@app.route('/job/<category>/<int:id>')
def vacancy_detail(category, id):
    context = {
        'vacancy': id,
        'category': category
    }
    return render_template('board/vacancy_detail.html', **context)
