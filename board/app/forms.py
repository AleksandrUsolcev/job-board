from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Email


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
    submit = SubmitField('Добавить категорию')
