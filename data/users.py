import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.Text, nullable=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.Text, nullable=True, unique=True)
    date_of_make = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    count_points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
