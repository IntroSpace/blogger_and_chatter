import os
from PIL import Image

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    visual_content = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    liked = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    def generate_blob(self, img):
        if not os.path.exists(os.path.join('static/img/posts', img)):
            return
        with open(os.path.join('static/img/posts', img), 'rb') as image:
            self.visual_content = image.read()
        os.remove(os.path.join('static/img/posts', img))
