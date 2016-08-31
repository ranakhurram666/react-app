"""
This module contains model classes of database entities.
"""
# 3rd party imports
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_, or_

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

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    path = db.Column(db.String)
    tag = db.Column(db.String)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Image Tag %r>' % self.tag

    def serialize(self, login_id):
        """
        Return object data in easily serializable format
        :type login_id: int
        :param login_id: Id of user who is logged in.

        """

        if self.user_id == login_id:
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

    @classmethod
    def get_image_data(cls):
        """
        This function returns Image data.
        :rtype: List of image objects
        """
        try:
            entries = Images.query.order_by(desc(Images.id)).all()
        except Exception:
            return "error"
        image_list = []

        [image_list.append(row.serialize(session['user'])) for row in entries]

        return image_list

    @classmethod
    def insert_data(cls, title, description, path, tag, category, user_id):
        """
        This function is inserting data in image table.
        :type title: str
        :param title: title of image
        :type description: str
        :param description: description of image
        :type path : str
        :param path: path of image
        :type tag: str
        :param tag: tag of image
        :type category: str
        :param category: category of image
        :type user_id: int
        :param user_id: user_id of user who uploaded image
        """
        title = str(title)
        description = str(description)
        path = str(path)
        tag = str(tag)
        category = str(category)
        new_image = Images(title=title, description=description, path=path, tag=tag, category=category, user_id=user_id)
        try:
            db.session.add(new_image)
            db.session.commit()
            return "inserted"
        except Exception:
            return "error"

    @classmethod
    def get_searched_data(cls, key):
        """
        This function searches Images on the basis of key.
        :type key: str
        :param key: Key to match the data.
        :return: Returns list of images whose tag, title and description contains key.
        """
        key = str(key)
        try:
            result = Images.query.filter(or_(Images.title.contains(key), Images.tag.contains(key),
                                         Images.description.contains(key))).all()
        except Exception:
            return "error"
        image_list = []

        [image_list.append(row.serialize(session['user'])) for row in result]
        return image_list

    @classmethod
    def get_category_data(cls, key):
        """
        Searching Images on the basis of category.
        :type key: str
        :param key: Category
        :return: Returns list of images whose category matches key.
        """
        key = str(key.strip())
        if key != "All":
            try:
                result = Images.query.filter_by(category=key).all()
            except Exception:
                return "error"
        else:
            try:
                result = Images.query.order_by(desc(Images.id)).all()
            except Exception:
                return "error"
        image_list = []
        [image_list.append(row.serialize(session['user'])) for row in result]
        return image_list

    @classmethod
    def email_existence(cls, email):
        """
        This function is checking either an email exist, during signup.
        :type email: str
        :param email: email to be checked
        """
        try:
            result = Users.query.filter_by(email=email).first()
        except Exception:
            return "error"
        if result is None:

            return True
        else:

            return False

    @classmethod
    def register_user(cls, name, password, email):
        """
        This function is registering the user.
        :type name: str
        :param name: Name of user
        :type password: str
        :param password: Password of user
        :type email: str
        :param email: Email of user
        """
        name = str(name)
        password = str(password)
        email = str(email)
        new_user = Users(name=name, password=password, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            return "error"

    @classmethod
    def get_authenticated(cls, email, password):
        """
        This function is authenticating user for Login.
        :type email: str
        :param email: Email of user
        :type password: str
        :param password: Password
        :return: Status of authentication.
        """
        try:
            result = Users.query.filter(and_(Users.email == str(email), Users.password == str(password))).all()
        except Exception:
            return "error"
        if result.__len__() < 1:
            return False
        else:
            session['user'] = result[0].id
            return True

    @classmethod
    def delete_image(cls, image_id):
        """
        This function deletes image. Accepts image id from delete route and deletes image.
        :type image_id: int
        :param image_id:
        """
        image_id = int(image_id)
        try:
            Images.query.filter(Images.id == image_id).delete()
            db.session.commit()
        except Exception:
            return "error"
