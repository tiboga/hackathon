from datetime import datetime

import sqlalchemy
from .users import User
from .db_session import SqlAlchemyBase


class TaskOfUsers(SqlAlchemyBase):
    __tablename__ = 'tasks_of_users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    user_answer = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    right_answer = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    resolved = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, nullable=True)