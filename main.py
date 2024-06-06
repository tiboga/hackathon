import os.path
import random
from generation import generate_example
from flask import Flask, render_template, redirect, flash, request, make_response, send_from_directory
from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from data import db_session, api
from data.users import User
import datetime
from profile_graphs import generate_progress_charts
from data.achievement_of_user import AchievementOfUser
from data.tasks_of_users import TaskOfUsers
from reward_for_achivments import generate_certificate

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
    if request.method == 'POST':
        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            task = db_sess.query(TaskOfUsers).filter(TaskOfUsers.id == current_user.current_task).first()
            task.user_answer = request.form['answer']
            db_sess.commit()
            if task.user_answer == task.right_answer:
                task.resolved = 1
                user = db_sess.query(User).filter(User.id == current_user.id).first()
                user.count_points += task.adding_points
                user.need_to_update_task = 1
                db_sess.commit()
                flash("Пример решен правильно", 'success')

            else:
                flash("Пример решен неправильно", 'danger')
            db_sess.commit()
            return redirect('/')
            # return render_template("main_page.html", a=a)
        else:
            if request.form['answer'] == request.cookies.get('right_answer'):
                flash('Пример решен правильно', 'success')
                return redirect('/')
            else:
                flash('Пример решен не правильно', 'danger')
                return render_template('main_page.html'
                                       , a=(request.cookies.get('task'),
                                            request.cookies.get('right_answer')
                                            ), missing=False)

    if request.method == 'GET':
        print()
        points_of_level = {'easy': 1,
                           'medium': 2,
                           'hard': 3}
        db_sess = db_session.create_session()
        if current_user.is_authenticated:
            flag = request.cookies.get('for_missing')
            if flag == "False":
                level = current_user.level_task
                type = current_user.type_task if current_user.type_task not in ['numerical',
                                                                                'equality'] else current_user.type_type_task
                a = generate_example(level=level, example_type=type)
                if current_user.need_to_update_task == 1:
                    task = TaskOfUsers()
                    task.user_answer = ''
                    task.right_answer = a[1]
                    task.task = a[0]
                    task.resolved = 0
                    task.user_id = current_user.id
                    task.adding_points = points_of_level[level] + 1
                    db_sess.add(task)
                    db_sess.commit()
                    user = db_sess.query(User).filter(User.id == current_user.id).first()
                    user.current_task = max(elem.id for elem in db_sess.query(TaskOfUsers).all())
                    user.need_to_update_task = 0
                    db_sess.commit()
                    return render_template("main_page.html", a=a)
                else:
                    current_task = db_sess.query(TaskOfUsers).filter(
                        TaskOfUsers.id == current_user.current_task).first()
                    return render_template('main_page.html', a=(current_task.task, current_task.right_answer),
                                           missing=False)
                # else:
                #     task = TaskOfUsers()
                #     task.user_answer = ''
                #     task.right_answer = a[1]
                #     task.task = a[0]
                #     task.resolved = 0
                #     task.user_id = current_user.id
                #     task.adding_points = points_of_level[level] + 1
                #     db_sess.add(task)
                #     db_sess.commit()
                #     user = db_sess.query(User).filter(User.id == current_user.id).first()
                #     user.current_task = max(elem.id for elem in db_sess.query(TaskOfUsers).all())
                #     db_sess.commit()
                #     return render_template("main_page.html", a=a)
            else:
                task = db_sess.query(TaskOfUsers).filter(TaskOfUsers.user_id == current_user.id,
                                                         TaskOfUsers.resolved == 0).first()
                if task:
                    user = db_sess.query(User).filter(User.id == current_user.id).first()
                    user.current_task = task.id
                    db_sess.commit()
                    return render_template('main_page.html', a=(task.task, task.right_answer), missing=True)
                return render_template("main_page.html", a=None, missing=True)
        else:
            level = random.randint(0, 2)
            a = generate_example(levels[level], action[random.randint(0, 5)])
            res = make_response(render_template('main_page.html', a=a, missing=False))
            res.set_cookie('right_answer', a[1], max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('task', a[0], max_age=60 * 60 * 24 * 365 * 2)
            return res


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
            TaskOfUsers.user_id == current_user.id,
            TaskOfUsers.date == elem,
            TaskOfUsers.resolved == 1).all()) for elem in dates]
        incorrect = [len(db_sess.query(TaskOfUsers).filter(
            TaskOfUsers.user_id == current_user.id,
            TaskOfUsers.date == elem,
            TaskOfUsers.resolved == 0).all()) for elem in dates]
        user_data = {
            'dates': dates,
            'correct': correct,
            'incorrect': incorrect
        }
        rewards = ['Отсутствует - с 15 баллов', 'Отсутствует - с 30 баллов', 'Отсутствует - с 45 баллов']
        if count_points >= 15:
            rewards[0] = 'Новобранец (15 баллов)'
        if count_points >= 30:
            rewards[1] = 'Молодец (30 баллов)'
        if count_points >= 45:
            rewards[2] = 'Гений (45 баллов)'
        filename = generate_progress_charts(user_data, correct_color='green', incorrect_color='orange',
                                            filename='graph.png')
        return render_template("profile.html", username=username, email=mail, points=count_points, greeting=greeting,
                               filename=filename, reward=rewards)
    flash('Вы ещё не вошли в аккаунт!', 'danger')
    return redirect("/")


@app.route("/top")
def top():
    db_sess = db_session.create_session()
    users_of_top = db_sess.query(User).all()
    users_of_top_10 = sorted(users_of_top, key=lambda x: x.count_points, reverse=True)[:10]
    dict_of_top10_user = dict()
    for i in range(10):
        if i < len(users_of_top_10):
            dict_of_top10_user[i + 1] = {"name": users_of_top_10[i].username,
                                         "countpoints": users_of_top_10[i].count_points}
        else:
            dict_of_top10_user[i + 1] = {"name": None,
                                         "countpoints": 0}
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
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            usernames_in_bd = db_sess.query(User).filter(User.username == newname).first()
            if not usernames_in_bd and len(newname) < 22:
                old_user = db_sess.query(User).filter(User.id == current_user.id).first()
                old_user.username = newname
                db_sess.commit()
                flash("'ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤНикнейм изменён!", 'success')
                return redirect('/profile')
            else:
                flash("Никнейм уже использован или его длина больше длины 22 символа", 'danger')
                return redirect('/change_data')
        return render_template('change_data.html', title='Смена данных')
    else:
        flash('Вы ещё не вошли в аккаунт!', 'danger')
        return redirect('/')


@login_required
@app.route('/missingexamples')
def missing_examples():
    db_sess = db_session.create_session()
    examples = [{'task': elem.task, 'user_answer': elem.user_answer, 'id': elem.id} for elem in
                db_sess.query(TaskOfUsers).filter(TaskOfUsers.user_id == current_user.id, TaskOfUsers.resolved == 0)]
    return render_template('missing_examples.html', examples=examples)


@login_required
@app.route("/changecurrenttask/<task_id>")
def change_current_task(task_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.current_task = task_id
    user.need_to_update_task = 0
    db_sess.commit()
    res = make_response(redirect('/'))
    res.set_cookie('for_missing', "True")
    return res


@login_required
@app.route("/setlevel/<level>")
def set_level(level):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.level_task = level
    user.need_to_update_task = 1
    db_sess.commit()
    return redirect("/")


@login_required
@app.route("/type/<type>")
def set_type(type):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.type_task = type
    if type == 'numerical':
        user.type_type_task = 'addition'
    if type == 'equality':
        user.type_type_task = 'equality'
    user.need_to_update_task = 1
    db_sess.commit()
    return redirect('/')


@login_required
@app.route("/typetypetask/<type>")
def set_type_of_type(type):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.type_type_task = type
    user.need_to_update_task = 1
    db_sess.commit()
    return redirect('/')


@login_required
@app.route('/outofmissings')
def out_of_missings():
    res = make_response(redirect('/'))
    res.set_cookie('for_missing', 'False')
    return res


@app.route('/skip')
def skip():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.need_to_update_task = 1
        print('skip')
        db_sess.commit()
    else:
        flash('Войдите в аккаунт для сохранения пропущенных примеров!', 'danger')
        return redirect('/')

    return redirect('/')


@app.route('/reward', methods=['GET', 'POST'])
def reward():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        username = user.username
        count_points = user.count_points
        if int(count_points) > 50:
            template_path = "Pinterest_Download (3).jpg"
            output_path = "certificate.png"
            name = username
            generate_certificate(name, template_path, output_path)
            return send_from_directory(os.path.dirname(output_path), os.path.basename(output_path), as_attachment=True)
        else:
            flash('ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤДля получения грамоты необходимо не менее 50 баллов рейтинга!', 'danger')
    else:
        flash('Войдите в аккаунт!', 'danger')
        return redirect('/')
    return redirect('/profile')


def main():
    if not os.path.exists('db'):
        os.mkdir('db')
    db_session.global_init("db/main.db")
    app.register_blueprint(api.blueprint)
    app.run("127.0.0.1", port=5000)


if __name__ == '__main__':
    main()
