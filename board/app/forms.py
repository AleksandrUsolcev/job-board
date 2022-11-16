from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, PasswordField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(FlaskForm):
    email = EmailField(
        'Электронная почта',
        validators=[DataRequired('Обязательное поле'),
                    Email('Неверный формат почты')]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired('Обязательное поле')]
    )
    submit = SubmitField('Вход')


class CategoryForm(FlaskForm):
    name = StringField(
        'Направление вакансии',
        validators=[DataRequired('Обязательное поле')]
    )
    description = TextAreaField('Описание', validators=[
                                DataRequired('Обязательное поле')])


class VacancyForm(FlaskForm):
    name = StringField(
        'Наименование вакансии',
        validators=[DataRequired('Обязательное поле')]
    )
    description = TextAreaField('Описание', validators=[
                                DataRequired('Обязательное поле')])
    requirements = TextAreaField('Требования', validators=[
        DataRequired('Обязательное поле')])
    min_exp = IntegerField('Минимальный опыт (лет)', validators=[Optional()])
    max_exp = IntegerField('Максимальный опыт (лет)', validators=[Optional()])
    count = IntegerField('Количество вакансий', validators=[
        DataRequired('Обязательное поле')])
    min_salary = IntegerField(
        'Минимальный оклад (руб)', validators=[Optional()])
    max_salary = IntegerField(
        'Максимальный оклад (руб)', validators=[Optional()])
