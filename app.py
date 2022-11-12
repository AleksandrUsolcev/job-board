from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'change-me'


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
    if request.method == 'POST':
        if request.form.get('password') != '12345':
            flash('Неверный пароль', category='error')
    context = {}
    return render_template('login.html', **context)


@app.route('/patients/<int:id>')
def patients_list(id):
    context = {
        'patient': id
    }
    return render_template('patient_page.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
