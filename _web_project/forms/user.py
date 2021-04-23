from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditPassword(FlaskForm):
    previous_password = StringField('Введите старый пароль')
    new_password = PasswordField('Ведите новый пароль')
    new_password_again = StringField('Повторите новый пароль')
    submit = SubmitField('Принять изменения')
