import requests
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, logout_user
from flask_restful import Api
from forms.users import LoginForm, RegisterForm
from data import db_session
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'
app.config['DATETIME_FORMAT'] = '%Y-%m-%d'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager(app)
login_manager.login_message = "Авторизация успешно выполнена"
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        return None
    return render_template("main_page.html")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login_page.html", title="Авторизация", form=form)


@app.route("/registration")
def registration():
    form = RegisterForm()
    return render_template("register_page.html", title="Регистрация", form=form)


@app.route("/profile")
def profile():
    return render_template("name_html.html")


@app.route("/top")
def top():
    return render_template("name_html.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/main.db")
    app.run("127.0.0.1", port=5000)


if __name__ == '__main__':
    main()
