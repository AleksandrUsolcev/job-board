from dotenv import load_dotenv
from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'change-me'


@app.errorhandler(Exception)
def error_page(error: Exception):
    error_list = [404, 401]
    if error.code not in error_list:
        return error
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
    test_password = '12345'
    test_email = 'admin@admin.admin'
    if request.method == 'POST':
        if request.form.get('password') != '12345':
            flash(request.form.get('email'), category='email')
            flash('Неверный пароль', category='error')
    context = {}
    if 'email' in session:
        return redirect(url_for('index'))
    elif (
        request.method == 'POST'
        and request.form.get('email') == test_email
        and request.form.get('password') == test_password
    ):
        session['email'] = test_email
        return redirect(url_for('index'))
    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


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


if __name__ == '__main__':
    app.run(debug=True)
