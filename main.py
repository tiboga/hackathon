from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask_project_secret_key'


@app.route('/')
def hello():
    return render_template("main_page.html")


def main():
    serve(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    print('Сайт запущен!')
    main()
    print('Сайт выключен!')
