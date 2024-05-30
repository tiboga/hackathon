import flask
from flask import jsonify, request, make_response

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/', methods=["POST"])
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
    dict_of_data = request.json
    if not all(key in request.json for key in
               ['login', 'password']):
        return make_response(jsonify({"ERROR": "incorrect json format. correct :{login:value, password:value}"}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == dict_of_data['login']).first()
    if user and user.check_password(dict_of_data['password']):
        return jsonify({'Status': 'ok', 'login': True})
    else:
        return jsonify({'Status': 'ok', 'login': False})

