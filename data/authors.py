import sqlalchemy
from .db_session import SqlAlchemyBase


authors_table = sqlalchemy.Table(
    'authors_table',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('projects', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('projects.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)
