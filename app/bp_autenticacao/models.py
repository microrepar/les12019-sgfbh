"""Módulo com os modelos - classe de domínio
"""
from app import db
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'tb_user'

    id = Column(Integer, primary_key=True)
    rgf = Column(Integer, index=True, unique=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    perfil = Column(String(50))
    password_hash = Column(String(128))
    last_seen = Column(DateTime, default=datetime.utcnow)
    about_me = Column(String(140))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
