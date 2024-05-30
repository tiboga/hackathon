import flask
from flask import jsonify, request, make_response
import generating_tasks
from data import db_session
from data.users import User
from data.tasks_of_users import TaskOfUsers

blueprint = flask.Blueprint(
    'api_hackathon',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/auth', methods=["POST"])
def add_user():
    dict_of_data = request.json
    if not all(key in request.json for key in
               ['login', 'username', 'password']):
        return make_response(jsonify({"ERROR": "incorrect json format"}), 400)
    else:
        db_sess = db_session.create_session()
        if "@" in dict_of_data['login']:
            if dict_of_data['login'].split("@")[0] == '' or dict_of_data['login'].split("@")[1] == '':
                return make_response(jsonify({"ERROR": "incorrect login format | example:s@s"}), 400)
        else:
            return make_response(jsonify({'Status': 'error', "description": "incorrect login format | example:s@s"}),
                                 400)
        sp_of_user = db_sess.query(User).all()

        if dict_of_data['login'] in [elem.login for elem in sp_of_user]:
            return make_response(jsonify({"Status": 'error', "description": "there is already such a login"}), 400)
        if dict_of_data['username'] in [elem.username for elem in sp_of_user]:
            return make_response(jsonify({"Status": 'error', "description": "there is already such a username"}), 400)
        user = User()
        user.login = dict_of_data['login']
        user.username = dict_of_data['username']
        user.set_password(dict_of_data['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'Status': 'ok'})


@blueprint.route('/api/user/login', methods=["POST"])
def login():
    dict_of_data = request.json # login, password
    if not all(key in request.json for key in
               ['login', 'password']):
        return make_response(jsonify(
            {"Status": "error", 'description': "incorrect json format. correct :{login:value, password:value}"}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == dict_of_data['login']).first()
    if user and user.check_password(dict_of_data['password']):
        return jsonify({'Status': 'ok', 'login': True, 'id': user.id})
    else:
        return jsonify({'Status': 'ok', 'login': False})


@blueprint.route("/api/task/new", methods=["POST"])
def new_task():
    dict_of_data = request.json # level, example_type, user_id
    if dict_of_data['level'] not in ('easy', 'medium', 'hard'):
        return jsonify(
            {"Status": "error", 'description':
                "level must be one of the values: ['easy', 'medium', 'hard']"})
    if dict_of_data['example_type'] not in (
    'addition', 'subtraction', 'multiplication', 'division', 'equality', 'quadratic', 'x_inequality'):
        return jsonify({"Status": "error",
                        'description': "example_type must be one of the values:"
                                       "['addition', 'subtraction', "
                                       "'multiplication', 'division', 'equality', 'quadratic', "
                                       "'x_inequality'}"})
    task = generating_tasks.generate_example(level=dict_of_data['level'], example_type=dict_of_data['example_type'])
    db_sess = db_session.create_session()
    task_of_user = TaskOfUsers()
    task_of_user.task = task[0]
    task_of_user.user_answer = ''
    task_of_user.right_answer = task[1]
    task_of_user.resolved = 0
    task_of_user.user_id = dict_of_data['user_id']
    db_sess.add(task_of_user)
    db_sess.commit()
    return jsonify({"Status": 'ok', 'task': task[0], 'answer': task[1]})
@blueprint.route('/api/task/change')
def change_task_answer():
    dict_of_data = request.json # user_id, task, new_answ
    try:
        db_sess = db_session.create_session()
        task_of_user = db_sess.query(TaskOfUsers).filter(TaskOfUsers.user_id==dict_of_data['user_id'], TaskOfUsers.task==dict_of_data['task']).all()
        task_of_user.user_answer = dict_of_data['new_answ']
        if task_of_user.user_answer == task_of_user.right_answer:
            task_of_user.resolved = 1
        db_sess.commit()
        return jsonify({'Status': 'ok'})
    except:
        return jsonify({"Status": "error"})
