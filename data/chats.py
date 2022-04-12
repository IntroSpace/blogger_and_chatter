import sqlalchemy
from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    users = sqlalchemy.Column(sqlalchemy.String)
    messages = sqlalchemy.Column(sqlalchemy.String, nullable=True)
