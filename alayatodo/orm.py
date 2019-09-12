from alayatodo import app, db
from flask_sqlalchemy import SQLAlchemy


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column('id', db.Integer, unique=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, default=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}