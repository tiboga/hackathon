import sqlalchemy
from .users import User
from .db_session import SqlAlchemyBase


class AchievementOfUser(SqlAlchemyBase):
    __tablename__ = 'tasks_of_users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    right_answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    resolved = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=True)
