from app import app, db
from app.admin import admin
from app.workspace import workspace

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(workspace, url_prefix='/workspace')

@app.shell_context_processor
def make_shell_context():
    context = {'db': db}
    return context


if __name__ == '__main__':
    app.run(debug=True)
