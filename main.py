import flask
import requests
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from flask_restful import Api
from forms.users import LoginForm, RegisterForm
from data import db_session
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'
login_manager = LoginManager(app)
login_manager.login_message = "Авторизация успешно выполнена"
login_manager.init_app(app)
api = Api(app)
blueprint = flask.Blueprint(
    'API_BD',
    __name__,
    template_folder='templates'
)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Клиентская часть
@app.route("/")
def main_page():
    return render_template("main_page.html")


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
            login_user(user)
            return redirect('/')
        flash("Неправильный логин или пароль", "danger")
        return render_template("login_page.html")
    return render_template("login_page.html", title='Авторизация')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт!', 'danger')
        return redirect('/')
    form = RegisterForm()
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
    return render_template("register_page.html", title="Регистрация", form=form)


@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        return render_template("profile.html")
    flash('Вы ещё не вошли в аккаунт!', 'danger')
    return redirect("/")


@app.route("/top")
def top():
    return render_template("name_html.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# Api


def main():
    db_session.global_init("db/main.db")
    # app.register_blueprint(API_BD.blueprint)
    app.run("127.0.0.1", port=5000)


if __name__ == '__main__':
    main()
