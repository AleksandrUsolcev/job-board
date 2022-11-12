from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    menu = ['test1', 'test2', 'test3']
    context = {
        'title': 'hello world',
        'menu': menu,
    }
    return render_template('index.html', **context)


@app.route('/patients')
def patients_list():
    return render_template('patients_list.html')


if __name__ == '__main__':
    app.run(debug=True)
