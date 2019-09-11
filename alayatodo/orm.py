from alayatodo import app, db
from flask_sqlalchemy import SQLAlchemy


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column('id', db.Integer, unique=True, nullable=False, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, default=False)
    