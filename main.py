import requests
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_restful import Api
from waitress import serve

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'
app.config['DATETIME_FORMAT'] = '%Y-%m-%d'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager(app)
login_manager.login_message = "Авторизация успешно выполнена"
login_manager.init_app(app)
api = Api(app)


@app.route("/")
def main_page():
    if current_user.is_authenticated:
        return None
    return render_template("index.html")


def main():
    serve(app, host="0.0.0.0", port=5000)
    # app.run("", port=5000)


if __name__ == '__main__':
    main()
