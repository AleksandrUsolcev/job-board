from app import app, db


@app.shell_context_processor
def make_shell_context():
    context = {'db': db}
    return context


if __name__ == '__main__':
    app.run(debug=True)
