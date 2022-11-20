from app.models import Candidate, Category, Vacancy
from app.workspace import workspace
from flask import render_template
from sqlalchemy import func


@workspace.route('/')
def index():
    candidates = Candidate.query.all()
    categories = Category.query.outerjoin(Vacancy).group_by(
        Category.id).order_by(func.count(Vacancy.id).desc()).all()
    context = {
        'candidates': candidates,
        'categories': categories
    }
    return render_template('workspace/index.html', **context)
