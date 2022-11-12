from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'change-me'


@app.errorhandler(404)
def not_found(error):
    context = {'error': error, 'error_code': 404}
    return render_template('error_page.html', **context), 404


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
    test_token = 'adksmdamasdmsakldmalsm'
    if request.method == 'POST':
        if request.form.get('password') != '12345':
            flash(request.form.get('email'), category='email')
            flash('Неверный пароль', category='error')
    context = {}
    if 'token' in session:
        return redirect(url_for('index'))
    elif (
        request.method == 'POST'
        and request.form.get('email') == test_email
        and request.form.get('password') == test_password
    ):
        session['token'] = test_token
        return redirect(url_for('index'))
    return render_template('login.html', **context)


@app.route('/patients/<int:id>')
def patients_list(id):
    check_token = session.get('token')
    if not check_token:
        abort(401)
    context = {'patient': id}
    return render_template('patient_page.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
