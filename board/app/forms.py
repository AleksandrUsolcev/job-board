from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, PasswordField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, NumberRange, Optional,
                                ValidationError)


class LoginForm(FlaskForm):
    email = EmailField(
        'Электронная почта',
        validators=[
            DataRequired('Обязательное поле'),
            Email('Неверный формат почты')
        ]
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
    description = TextAreaField(
        'Описание',
        validators=[DataRequired('Обязательное поле')]
    )


class VacancyForm(FlaskForm):
    name = StringField(
        'Наименование вакансии',
        validators=[DataRequired('Обязательное поле')]
    )
    description = TextAreaField(
        'Описание',
        validators=[DataRequired('Обязательное поле')]
    )
    requirements = TextAreaField(
        'Требования',
        validators=[DataRequired('Обязательное поле')]
    )
    min_exp = IntegerField(
        'Минимальный опыт (лет)',
        validators=[
            Optional(),
            NumberRange(
                min=1,
                max=15,
                message='Допустимый диапазон значений от 1 до 15'
            )
        ]
    )
    max_exp = IntegerField(
        'Максимальный опыт (лет)',
        validators=[
            Optional(),
            NumberRange(
                min=1,
                max=15,
                message='Допустимый диапазон значений от 1 до 15'
            )
        ]
    )
    count = IntegerField(
        'Количество вакансий',
        validators=[
            DataRequired('Обязательное поле'),
            NumberRange(
                min=1,
                max=10,
                message='Допустимый диапазон значений от 1 до 10'
            )
        ]
    )
    min_salary = IntegerField(
        'Минимальный оклад (руб)',
        validators=[
            Optional(),
            NumberRange(
                min=20000,
                max=10000000,
                message='Допустимый диапазон значений от 20 000 до 10 000 000'
            )
        ]
    )
    max_salary = IntegerField(
        'Максимальный оклад (руб)',
        validators=[
            Optional(),
            NumberRange(
                min=20000,
                max=10000000,
                message='Допустимый диапазон значений от 20 000 до 10 000 000'
            )
        ]
    )

    def validate_min_exp(form, field):
        max_exp = form.data.get('max_exp')
        error = 'Минимальное значение не должно превышать максимальное'
        if max_exp and field.data >= max_exp:
            raise ValidationError(error)

    def validate_min_salary(form, field):
        max_salary = form.data.get('max_salary')
        error = 'Минимальное значение не должно превышать максимальное'
        if max_salary and field.data >= max_salary:
            raise ValidationError(error)
