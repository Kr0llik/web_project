import os

import flask_login
import requests
from flask import Flask, render_template, redirect, request
from flask_login import login_user, LoginManager, \
    current_user, login_required, logout_user

from forms.user import RegisterForm, LoginForm
from data.users import User
from PIL import Image
from urllib.request import urlopen
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def conversion_for_q1(res):
    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == res.count('1'):
        return 'Detective'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == res.count('2'):
        return 'Fantastic'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == res.count('3'):
        return 'Thriller'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == res.count('4'):
        return 'Romance'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == \
            res.count('1') == res.count('3'):
        return 'Psychology'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == \
            res.count('1') == res.count('4'):
        return 'Adventures'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == \
            res.count('2') == res.count('3'):
        return 'Horror'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == \
            res.count('2') == res.count('4'):
        return 'Fantasy'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6')) == \
            res.count('3') == res.count('4'):
        return 'Classic'


def conversion_for_q2(res):
    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == res.count('1'):
        return 'Detective'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == res.count('2'):
        return 'Fantastic'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == res.count('3'):
        return 'Thriller'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == res.count('4'):
        return 'Romance'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == \
            res.count('1') == res.count('3'):
        return 'Psychology'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == \
            res.count('1') == res.count('4'):
        return 'Adventures'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == \
            res.count('2') == res.count('3'):
        return 'Horror'

    if max(res.count('1'), res.count('2'), res.count('3'),
           res.count('4'), res.count('5'), res.count('6'),
           res.count('7'), res.count('8'), res.count('9'),
           res.count('10')) == \
            res.count('2') == res.count('4'):
        return 'Fantasy'

    return 'Classic'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/project_db.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template('tst.html', title='Мандаринка', message='Это пока что недоступно')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            results=''
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=LoginForm().remember_me.data)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data) \
                and user.name == form.name.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин, email или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/personal_acc', methods=['GET', 'POST'])
def personal_acc():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == flask_login.current_user.email).first()
    if request.method == 'GET':
        return render_template('personal_ac.html', title='Личный кабинет',
                               name=user.name, password='2', flag=0,
                               date=user.created_date.strftime('%d %b %Y'), email=flask_login.current_user.email)
    elif request.method == 'POST':
        return render_template('personal_ac.html', title='Личный кабинет',
                               name=user.name, password='2',
                               flag=int(request.form['type']),
                               date=user.created_date.strftime('%d %b %Y'), email=flask_login.current_user.email)


@app.route('/subjects/<string:genre>', methods=['GET', 'POST'])
def subjects(genre):
    if not current_user.is_authenticated:
        return redirect('/')
    if genre.capitalize() not in ['Detective', 'Fantastic',
                                  'Thriller', 'Romance',
                                  'Psychology',
                                  'Adventures', 'Horror',
                                  'Fantasy', 'Classic']:
        return redirect('/')

    if request.method == 'GET':
        tmp_list = []
        respone = requests.get(f"http://openlibrary.org/subjects/{genre.lower()}.json").json()
        q = 0
        for x in respone['works']:
            respone_new = requests.get(f"http://openlibrary.org{x['key']}.json")
            if f'static/img/{genre.lower()}{q}.jpg' not in os.listdir(f"{os.getcwd()}/static/img"):
                img = Image.open(urlopen(f"http://covers.openlibrary.org/b/id/{x['cover_id']}-L.jpg"))
                img = img.convert('RGB')
                img.save(f'static/img/{genre.lower()}{q}.jpg')
            if 'description' in respone_new.json().keys():
                if type(respone_new.json()['description']) is str:
                    tmp_list.append((respone_new.json()['description'],
                                     f"{x['authors'][0]['name']} - {x['title']}"))
                elif type(respone_new.json()['description']) is dict and 'value' in \
                        respone_new.json()['description'].keys():
                    tmp_list.append((respone_new.json()['description']['value'],
                                     f"{x['authors'][0]['name']} - {x['title']}"))
            q += 1

        return render_template('resultss.html', title='Мандаринка',
                               genre=genre, values=tmp_list)


@app.route('/questionnaire_menu', methods=['GET', 'POST'])
def questionnaire_menu():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = db_session.create_session()
    res_d = db_sess.query(User).filter(User.email == flask_login.current_user.email).first()
    if not bool(res_d.results):
        first = False
        second = False
        third = False
    else:
        first = res_d.results.split('|')[0]
        if len(res_d.results.split('|')) == 3 and \
                bool(res_d.results.split('|')[1]):
            second = res_d.results.split('|')[1]
        else:
            second = False
        if len(res_d.results.split('|')) == 3:
            third = res_d.results.split('|')[2]
        else:
            third = False

    if request.method == 'GET':
        return render_template('menu.html', title='Мандаринка',
                               first=first,
                               second=second,
                               third=third)
    elif request.method == 'POST':
        return render_template('menu.html', title='Мандаринка',
                               flag=request.form['type'],
                               first=first,
                               second=second,
                               third=third)


@app.route('/questionnarie1', methods=['GET', 'POST'])
def questionnarie1():
    if not current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('questionnarie.html', title='Мандаринка')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        res_d = db_sess.query(User).filter(User.email == flask_login.current_user.email).first()

        res_d.results = conversion_for_q1(str(request.form['question1'] +
                                              request.form['question2'] +
                                              request.form['question3'] +
                                              request.form['question4'] +
                                              request.form['question5'] +
                                              request.form['question6'])) + \
                        '|' + res_d.results

        res_d.results = '|'.join(res_d.results.split('|')[:3:])

        db_sess.commit()

        return redirect('/')


@app.route('/questionnarie2', methods=['GET', 'POST'])
def questionnarie2():
    if not current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('questionnarie2.html', title='Мандаринка')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        res_d = db_sess.query(User).filter(User.email == flask_login.current_user.email).first()

        res_d.results = conversion_for_q2(str(request.form['question1'] +
                                              request.form['question2'] +
                                              request.form['question3'] +
                                              request.form['question4'] +
                                              request.form['question5'] +
                                              request.form['question6'] +
                                              request.form['question7'] +
                                              request.form['question8'] +
                                              request.form['question9'] +
                                              request.form['question10'])) + \
                        '|' + res_d.results

        res_d.results = '|'.join(res_d.results.split('|')[:3:])

        db_sess.commit()

        return redirect('/')


@app.route('/questionnarie3', methods=['GET', 'POST'])
def questionnarie3():
    if not current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('opr3.html', title='Мандаринка')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        res_d = db_sess.query(User).filter(User.email == flask_login.current_user.email).first()

        res_d.results = conversion_for_q2(str(request.form['question1'] +
                                              request.form['question2'] +
                                              request.form['question3'] +
                                              request.form['question4'] +
                                              request.form['question5'] +
                                              request.form['question6'] +
                                              request.form['question7'] +
                                              request.form['question8'] +
                                              request.form['question9'] +
                                              request.form['question10'])) + \
                        '|' + res_d.results

        res_d.results = '|'.join(res_d.results.split('|')[:3:])

        db_sess.commit()

        return redirect('/')


@app.route('/facts', methods=['GET', 'POST'])
def facts():
    if not current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('if.html', title='Мандаринка')



if __name__ == '__main__':
    main()
