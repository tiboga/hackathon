import random
from generation import generate_example
import flask
import requests
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from forms.users import LoginForm, RegisterForm
from data import db_session, api
from data.users import User
import datetime
from data.achievement_of_user import AchievementOfUser
import datetime
from profile_graphs import generate_progress_charts
from data.achievement_of_user import AchievementOfUser
from data.tasks_of_users import TaskOfUsers

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'
login_manager = LoginManager(app)
login_manager.login_message = "Авторизация успешно выполнена"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


# Клиентская часть
@app.route("/", methods=['GET', 'POST'])
def main_page():
    levels = ['easy', 'medium', 'hard']
    action = ['addition', 'subtraction', 'multiplication', 'division', 'equality', 'quadratic']
    a = generate_example(levels[random.randint(0, 2)], action[random.randint(0, 5)])
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        task = TaskOfUsers()
        task.user_answer = ''
        task.right_answer = a[1]
        task.task = a[0]
        task.resolved = 0
        task.user_id = current_user.id
        db_sess.add(task)
        db_sess.commit()
    if request.method == 'POST':
        db_sess = db_session.create_session()
    return render_template("main_page.html", a=a)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт!', 'danger')
        return redirect("/")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Вы успешно вошли в аккаунт!', 'success')
            return redirect('/')
        flash("Неправильный логин или пароль", "danger")
        return render_template("login_page.html")
    return render_template("login_page.html", title='Авторизация')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт!', 'danger')
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        db_sess = db_session.create_session()
        usernames_in_bd = db_sess.query(User).filter(User.username == username).first()
        emails_in_bd = db_sess.query(User).filter(User.login == email).first()
        if not usernames_in_bd and not emails_in_bd and len(username) < 22:
            user = User(login=email, username=username, count_points=0)
            user.set_password(password)
            db_sess.add(user)
            db_sess.commit()
            login_user(user, remember=True)
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect('/')
        elif usernames_in_bd:
            flash('Такое имя пользователя уже зарегистрировано!', 'danger')
        elif emails_in_bd:
            flash('Такой адрес электронной почты уже зарегистрирован!', 'danger')
        elif len(username) > 21:
            flash('Никнейм не может быть длиннее, чем 21 символ!', 'danger')
        else:
            pass
    return render_template('register_page.html', title='Регистрация')


'''    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        usernames_in_bd = db_sess.query(User).filter(User.username == form.username.data).first()
        logins_in_bd = db_sess.query(User).filter(User.login == form.login.data).first()
        if form.password.data == form.repeat_password.data and not usernames_in_bd and not logins_in_bd:
            user = User(login=form.login.data, username=form.username.data, count_points=0)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
        else:
            pass
    return render_template("register_page.html", title="Регистрация", form=form)'''


@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        username = user.username
        mail = user.login
        count_points = user.count_points
        count_achievements = db_sess.query(AchievementOfUser).count()
        now = datetime.datetime.now()
        if now.hour >= 6 and now.hour < 12:
            greeting = 'Доброе утро,'
        elif now.hour >= 12 and now.hour < 18:
            greeting = 'Добрый день,'
        elif now.hour >= 18 and now.hour < 24:
            greeting = 'Добрый вечер,'
        else:
            greeting = 'Доброй ночи,'
        dates = [str(datetime.datetime.now().date() - datetime.timedelta(days=i)) for i in range(5)]
        dates.reverse()
        print(dates)
        db_sess = db_session.create_session()
        correct = [len(db_sess.query(TaskOfUsers).filter(
            TaskOfUsers.user_id==current_user.id,
            TaskOfUsers.date==elem,
            TaskOfUsers.resolved==1).all()) for elem in dates]
        incorrect = [len(db_sess.query(TaskOfUsers).filter(
            TaskOfUsers.user_id==current_user.id,
            TaskOfUsers.date==elem,
            TaskOfUsers.resolved==0).all()) for elem in dates]
        user_data = {
            'dates': dates,
            'correct': correct,
            'incorrect':incorrect
        }
        filename = generate_progress_charts(user_data, correct_color='green', incorrect_color='orange',
                                            filename='graph.png')
        return render_template("profile.html", username=username, email=mail, points=count_points, greeting=greeting,
                               filename=filename)
    flash('Вы ещё не вошли в аккаунт!', 'danger')
    return redirect("/")


@app.route("/top")
def top():
    db_sess = db_session.create_session()
    users_of_top = db_sess.query(User).all()
    print(users_of_top)
    users_of_top_10 = sorted(users_of_top, key=lambda x: x.count_points, reverse=True)[:10]
    dict_of_top10_user = dict()
    for i in range(10):
        if i < len(users_of_top_10):
            dict_of_top10_user[i + 1] = {"name": users_of_top_10[i].username,
                                         "countpoints": users_of_top_10[i].count_points}
        else:
            dict_of_top10_user[i + 1] = {"name": None,
                                         "countpoints": 0}
    print(dict_of_top10_user)
    return render_template("raiting.html", top_users=dict_of_top10_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/change_data', methods=["GET", "POST"])
def change_data():
    if current_user.is_authenticated:
        if request.method == 'POST':
            newname = request.form['nickname']
            password = request.form['password']
            db_sess = db_session.create_session()
            usernames_in_bd = db_sess.query(User).filter(User.username == newname).first()
            if not usernames_in_bd and len(newname) < 22:
                old_user = db_sess.query(User).filter(User.id == current_user.id).first()
                old_user.username = newname
                db_sess.commit()
                flash("Океоке", 'success')
                return redirect('/profile')
            else:
                flash("Неокенеоке", 'danger')
                return redirect('/change_data')
        return render_template('change_data.html', title='Смена данных')
    else:
        flash('Вы ещё не вошли в аккаунт!', 'danger')
        return redirect('/')

@login_required
@app.route('/missingexamples')
def missing_examples():
    db_sess = db_session.create_session()
    examples = [{'task': elem.task, 'user_answer':elem.user_answer, 'resolved': elem.resolved}for elem in  db_sess.query(TaskOfUsers).filter(TaskOfUsers.user_id==current_user.id, TaskOfUsers.resolved==0)]
    return examples
# Api
def main():
    db_session.global_init("db/main.db")
    app.register_blueprint(api.blueprint)
    app.run("127.0.0.1", port=5000)


if __name__ == '__main__':
    main()
