import requests
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_restful import Api
from waitress import serve
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
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def main_page():
    if current_user.is_authenticated:
        return None
    return render_template("index.html")


def main():
    app.run("127.0.0.1", port=5000)


if __name__ == '__main__':
    main()
