import datetime
import os
from PIL import Image

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    avatar = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    admin_status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    post = orm.relation("Post", back_populates='user')
    comment = orm.relation("Comment", back_populates='user')

    def generate_blob(self, img):
        if not os.path.exists(os.path.join('static/img/avatars', img)):
            return
        image = Image.open(os.path.join('static/img/avatars', img))
        w, h = image.size
        if w != h:
            center_x, center_y = w // 2, h // 2
            base_size = min(w, h) // 2
            image = image.crop((center_x - base_size, center_y - base_size,
                                center_x + base_size, center_y + base_size))
        if w > 128 or h > 128:
            image = image.resize((128, 128), Image.ANTIALIAS)
        image.save(os.path.join('static/img/avatars', img))
        with open(os.path.join('static/img/avatars', img), 'rb') as image:
            self.avatar = image.read()
        os.remove(os.path.join('static/img/avatars', img))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
