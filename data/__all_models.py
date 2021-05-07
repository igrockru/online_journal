import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, orm
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, \
    BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Klass(SqlAlchemyBase, UserMixin):
    __tablename__ = 'klass'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    kl_name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

    def __repr__(self):
        return f'<kl_name> {self.kl_name}'


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kod = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rega = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    klass = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("klass.id"))

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Klass_works(SqlAlchemyBase, UserMixin):
    __tablename__ = 'klass_works'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    klass = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("klass.id"))
    work_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<name> {self.name}'


class Marks(SqlAlchemyBase, UserMixin):
    __tablename__ = 'marks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("users.id"))
    work = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("klass_work.id"))
    mark = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    surname = StringField('Ваша фамилия (с большой буквы)',
                          validators=[DataRequired()])
    name = StringField('Ваше имя (с большой буквы)',
                       validators=[DataRequired()])
    kod = StringField('Ваш код', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class Check_del(FlaskForm):
    pass


class Klass_del(FlaskForm):
    klass = StringField('Какой класс удалить', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class Klass_add(FlaskForm):
    klass = StringField('Какой класс добавить', validators=[DataRequired()])
    submit = SubmitField('Добавить')
