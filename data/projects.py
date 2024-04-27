import datetime
import sqlalchemy
from sqlalchemy import orm

from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy.dialects.mysql import LONGTEXT


class Projects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'projects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    annotation = sqlalchemy.Column(LONGTEXT, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    docs_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    authors_users = orm.relationship("Users", secondary="authors", backref="projects")
