from datetime import datetime

import sqlalchemy
from .users import User
from .db_session import SqlAlchemyBase


class TaskOfUsers(SqlAlchemyBase):
    __tablename__ = 'tasks_of_users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user_answer = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    right_answer = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    resolved = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Text, default=datetime.now().date(), nullable=True)
    adding_points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)