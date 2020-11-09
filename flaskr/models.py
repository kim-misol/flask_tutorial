from flaskr import db, bcrypt, ma
from sqlalchemy import func, cast, Column, Integer, Text, DateTime, ForeignKey, String, Boolean, ARRAY, inspect, \
    Unicode, select, case, Enum, JSON
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref, synonym
from sqlalchemy.ext.hybrid import hybrid_property
import click
from flask.cli import with_appcontext


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, index=True)
    _password = Column(String(128), nullable=False)
    email = Column(Text, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True))
    createdAt = synonym('created_at')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    content_json = Column(JSON)
    content_preview = Column(Text)
    attachment = Column(Text)
    save_type = Column(Text)
    created_at = Column(DateTime(timezone=True))
    createdAt = synonym('created_at')
    modified_at = Column(DateTime(timezone=True))
    modifiedAt = synonym('modified_at')
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    userId = synonym('user_id')


def create():
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    table_list = ['post', 'users']
    for t in table_list:
        if t not in db.engine.table_names():
            create()
            break
    click.echo('Initialized the database.')


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    create()
    click.echo('Reset the database.')
