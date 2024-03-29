from app import app, db
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from slugify import slugify
from sqlalchemy import func
from werkzeug.urls import url_parse

from .forms import CategoryForm, LoginForm, RespondForm, VacancyForm
from .models import Candidate, Category, User, Vacancy


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
    categories = Category.query.outerjoin(Vacancy).group_by(
        Category.id).order_by(func.count(Vacancy.id).desc()).all()
    context = {
        'title': 'Job Board',
        'categories': categories
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
        slug = slugify(form.name.data)
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


@app.route('/job/<category>/edit', methods=['GET', 'POST'])
@login_required
def category_edit(category):
    category_url = category
    category = Category.query.filter_by(slug=category).first()
    if not category:
        abort(404)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        slug = slugify(form.name.data)
        category.name = form.name.data
        category.description = form.description.data
        category.slug = slug
        db.session.commit()
        return redirect(url_for('category_detail', category=slug), 301)
    context = {
        'form': form,
        'is_edit': True,
        'category_url': category_url,
        'category': category
    }
    return render_template('board/category_add.html', **context)


@app.route('/job/<category>')
def category_detail(category):
    category_url = category
    category = Category.query.filter_by(slug=category).first()
    if not category:
        abort(404)
    context = {
        'category': category,
        'category_url': category_url
    }
    return render_template('board/category_detail.html', **context)


@app.route('/job/<category>/add', methods=['GET', 'POST'])
@login_required
def vacancy_add(category):
    category_url = category
    category = Category.query.filter_by(slug=category).first()
    form = VacancyForm()
    form.category_id.data = category
    if not category:
        abort(404)
    if form.validate_on_submit():
        data = form.data
        slug = slugify(form.name.data)
        data.pop('csrf_token', None)
        data.pop('category_id', None)
        vacancy = Vacancy(
            author_id=current_user.id,
            slug=slug,
            category_id=category.id,
            **data
        )
        db.session.add(vacancy)
        db.session.commit()
        return redirect(
            url_for(
                'vacancy_detail',
                category=category_url,
                vacancy=slug), 301
        )
    context = {
        'category': category,
        'form': form,
        'category_url': category_url
    }
    return render_template('board/vacancy_add.html', **context)


@app.route('/job/<category>/<vacancy>/edit', methods=['GET', 'POST'])
@login_required
def vacancy_edit(category, vacancy):
    category_url = category
    vacancy_url = vacancy
    vacancy = Vacancy.query.filter_by(slug=vacancy).first()
    if not vacancy:
        abort(404)
    category = Category.query.filter_by(id=vacancy.category_id).first()
    if category.slug != category_url.lower():
        abort(404)
    form = VacancyForm(obj=vacancy)
    if not form.validate_on_submit() and not form.errors:
        form.category_id.data = category
    if form.validate_on_submit():
        slug = slugify(form.name.data)
        vacancy.slug = slug
        vacancy.category_id = form.category_id.data.id
        data = form.data
        data.pop('category_id', None)
        for key, value in data.items():
            setattr(vacancy, key, value)
        db.session.commit()
        return redirect(
            url_for(
                'vacancy_detail',
                category=form.category_id.data.slug,
                vacancy=slug), 301
        )
    context = {
        'category': category,
        'vacancy': vacancy,
        'form': form,
        'category_url': category_url,
        'vacancy_url': vacancy_url,
        'is_edit': True
    }
    return render_template('board/vacancy_add.html', **context)


@app.route('/job/<category>/<vacancy>')
def vacancy_detail(category, vacancy):
    category_url = category
    vacancy_url = vacancy
    vacancy = Vacancy.query.filter_by(slug=vacancy).first()
    if not vacancy:
        abort(404)
    category = Category.query.filter_by(id=vacancy.category_id).first()
    if category.slug != category_url.lower():
        abort(404)
    context = {
        'vacancy': vacancy,
        'category': category,
        'category_url': category_url,
        'vacancy_url': vacancy_url,
    }
    return render_template('board/vacancy_detail.html', **context)


@app.route('/job/<category>/<vacancy>/respond', methods=['GET', 'POST'])
def vacancy_respond(category, vacancy):
    category_url = category
    vacancy_url = vacancy
    vacancy = Vacancy.query.filter_by(slug=vacancy).first()
    if not vacancy:
        abort(404)
    category = Category.query.filter_by(id=vacancy.category_id).first()
    if category.slug != category_url.lower():
        abort(404)
    form = RespondForm()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        candidate = Candidate(
            vacancy_id=vacancy.id,
            **data
        )
        db.session.add(candidate)
        db.session.commit()
        return redirect(
            url_for(
                'vacancy_detail',
                category=category_url,
                vacancy=vacancy_url
            ), 301
        )
    context = {
        'category': category,
        'vacancy': vacancy,
        'form': form,
        'category_url': category_url,
        'vacancy_url': vacancy_url
    }
    return render_template('board/vacancy_respond.html', **context)
