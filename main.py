from data import db_session
from flask import Flask, render_template, redirect
from data.__all_models import User, Klass, Klass_works, Marks, LoginForm, \
    RegisterForm, Check_del, Klass_del, Klass_add
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/user_self_del')
@login_required
def user_self_del():
    form = Check_del()
    return render_template('check_del.html', title='Удаление аккаунта',
                           form=form)


@app.route('/klass_del', methods=['GET', 'POST'])
@login_required
def klass_del():
    form = Klass_del()
    if form.validate_on_submit():
        klass_list = db_sess.query(Klass).all()
        klass_l = []
        for item in klass_list:
            klass_l.append(item.kl_name)
        if str(form.klass.data) not in klass_l:
            return render_template('klass_del.html', title='Удаление класса',
                                   form=form,
                                   message="Нет такого класса")
        else:
            kl = db_sess.query(Klass).filter(
                Klass.kl_name == form.klass.data).first()
            check_list = db_sess.query(User).filter(User.klass == kl.id).all()
            if len(check_list) > 0:
                return render_template('klass_del.html',
                                       title='Удаление класса',
                                       form=form,
                                       message="Невозможно удалить класс, есть ученики этого класса в БД")
            else:
                db_sess.delete(kl)
                db_sess.commit()
                return redirect("/")

    return render_template('klass_del.html', title='Удаление класса',
                           form=form)


@app.route('/klass_add', methods=['GET', 'POST'])
@login_required
def klass_add():
    form = Klass_add()
    if form.validate_on_submit():
        kl = db_sess.query(Klass).filter(
            Klass.kl_name == form.klass.data).all()
        if len(kl) > 0:
            return render_template('klass_add.html', title='Добавление класса',
                                   form=form,
                                   message="Такой класс уже есть")
        else:
            new = Klass(kl_name=form.klass.data)
            db_sess.add(new)
            db_sess.commit()
            return redirect("/")
    return render_template('klass_add.html', title='Добавление класса',
                           form=form)


@app.route('/user_self_del_yes')
@login_required
def user_self_del_yes():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.email = None
    user.hashed_password = None
    user.rega = 'нет'
    db_sess.commit()
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print('Пароли')
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data,
                                      User.rega == 'да').first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="вы уже регистрировались")
        if db_sess.query(User).filter(User.name == form.name.data,
                                      User.surname == form.surname.data,
                                      User.kod != form.kod.data,
                                      User.rega == 'нет').first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="неверный код")
        if db_sess.query(User).filter(User.name == form.name.data,
                                      User.surname == form.surname.data,
                                      User.kod == form.kod.data).first() is None:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Вы еще не были внесены в базу данных учителем")

        if db_sess.query(User).filter(User.name == form.name.data,
                                      User.surname == form.surname.data,
                                      User.kod == form.kod.data,
                                      User.rega == 'нет').first():
            print('тут', form.name.data, form.surname.data, form.kod.data)
            user = db_sess.query(User).filter(User.name == form.name.data,
                                              User.surname == form.surname.data).first()
            print(user.name, user.surname, user.kod)
            user.set_password(form.password.data)
            user.email = form.email.data
            user.rega = 'да'
            db_sess.commit()
            return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
def marks_log():
    db_sess = db_session.create_session()
    marks_r = []
    marks_l = []
    if current_user.is_authenticated and current_user.id != 1:
        marks_r = db_sess.query(Marks).filter(
            Marks.user == current_user.id).all()
        for item in marks_r:
            res = db_sess.query(Klass_works).filter(
                Klass_works.id == item.work).first()
            name = res.name
            date = res.work_date
            marks_l.append((date, name, item.mark, item.id))
        marks_l.sort(key=lambda s: s[3])
        return render_template("marks_log.html", marks_list=marks_l)
    if current_user.is_authenticated and current_user.id == 1:
        klass_l = db_sess.query(Klass).all()
        return render_template("admin_page.html", klass_list=klass_l)
    return redirect('/login')

if __name__ == '__main__':
    db_session.global_init("db/my_base.db")
    db_sess = db_session.create_session()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

#if __name__ == '__main__':
    #db_session.global_init("db/my_base.db")
    #db_sess = db_session.create_session()
    #app.run(port=8080, host='127.0.0.1')
