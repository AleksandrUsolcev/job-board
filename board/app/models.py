from datetime import datetime

from app import db, login
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(640), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)

    vacancies = db.relationship('Vacancy', backref='category', lazy='dynamic')

    @property
    def vacancies_quantity(self):
        return self.vacancies.with_entities(
            func.sum(Vacancy.quantity)).scalar()

    def __repr__(self):
        return f'<Category {self.name}>'


class Vacancy(db.Model):
    __tablename__ = 'vacancies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    requirements = db.Column(db.Text(), nullable=False)
    min_exp = db.Column(db.Integer)
    max_exp = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'),
        nullable=False)

    candidates = db.relationship(
        'Candidate', backref='vacancy', lazy='dynamic')

    def __repr__(self):
        return f'<Vacancy {self.name}>'


class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telegram = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.Text())
    vacancy_id = db.Column(
        db.Integer, db.ForeignKey('vacancies.id'),
        nullable=False)

    def __repr__(self):
        return f'<Candidate {self.name}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
