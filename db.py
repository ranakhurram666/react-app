from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)


class Users(db.Model):
    """
    Users model class
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return self.id

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email
        }


class Images(db.Model):
    """
    Images model class
    """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    path = db.Column(db.String)
    tag = db.Column(db.String)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Image Tag %r>' % self.tag

    def serialize(self, id):
        """Return object data in easily serializeable format"""
        delete = ""
        if self.user_id == id:
            delete = 'yes'
        else:
            delete = 'no'
        return {
            'id': self.id,
            'tag': self.tag,
            'description': self.description,
            'title': self.title,
            'path': self.path,
            'category': self.category,
            'delete': delete
        }
