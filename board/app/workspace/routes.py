from app.models import Candidate, Category, Vacancy
from app.workspace import workspace
from flask import render_template
from sqlalchemy import func
from flask_login import login_required


@workspace.route('/')
@login_required
def index():
    candidates = Candidate.query.all()
    categories = Category.query.outerjoin(Vacancy).group_by(
        Category.id).order_by(func.count(Vacancy.id).desc()).all()
    context = {
        'candidates': candidates,
        'categories': categories
    }
    return render_template('workspace/index.html', **context)
