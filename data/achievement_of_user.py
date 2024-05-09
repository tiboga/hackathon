import sqlalchemy
from .users import User
from .achievement import Achievement
from .db_session import SqlAlchemyBase
import datetime

class AchievementOfUser(SqlAlchemyBase):
    __tablename__ = 'achievement_of_user'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=True)
    ach_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Achievement.id), nullable=True)
    date_ach = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now, nullable=True)