from flask import render_template
from app.admin import admin


@admin.route('/')
def index():
    return render_template('admin/index.html')
