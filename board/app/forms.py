from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
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
