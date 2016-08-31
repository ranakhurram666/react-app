"""
This module contains server side flask coding.
"""
# Builtin Imports
import os
from flask import Flask, request, session, g, redirect, url_for, \
     render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from PilLite import Image
import requests
import requests.packages.urllib3
from sqlalchemy import desc, and_, or_
# Importing self made Model classes
from db import db, Images, Users

requests.packages.urllib3.disable_warnings()


# Initializing Environment variables for app
app = Flask(__name__)
app.config.from_object(__name__)
UPLOAD_FOLDER = 'static/css/img'
LINK_FOLDER = '../static/css/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
CORS(app)
db.create_all()


@app.route('/')
def hello_world():
    return render_template('login.html')


def insert_data(title, description, path, tag, category, user_id):
    """
    This function is inserting data in image table.
    :param title: title of image
    :param description: description of image
    :param path: path of image
    :param tag: tag of image
    :param category: category of image
    :param user_id: user_id ofo user who uploaded image
    """
    title = str(title)
    description = str(description)
    path = str(path)
    tag = str(tag)
    category = str(category)
    new_image = Images(title=title, description=description, path=path, tag=tag, category=category, user_id=user_id)
    db.session.add(new_image)
    db.session.commit()


def get_image_data():
    """
    This function is returning Image data.
    """
    entries = Images.query.order_by(desc(Images.id)).all()
    image_list = []
    for row in entries:
        image_list.append(row.serialize(session['user']))

    return image_list


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    """
    This function is uploading image to sever and storing its object in database. In this function Image is
    converted in to .png by extracting 1st frame of original image. For given urls of images, image is downloaded from
    url and converted into .png
    :return: This function return list of all images after uploading
    """
    file_data = ""
    filename = ""
    temp_file_name = ""
    image_form_data = request.form
    print(image_form_data)
    if image_form_data.get('radios') == '1':
        files = request.files
        file_data = files['gif']
        filename = secure_filename(file_data.filename)
        temp_file_name = filename.rsplit('.', 1)
        temp_file_name = temp_file_name[0]
        file_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        remote = requests.get(image_form_data.get('image_url'), verify=False)
        max_id = db.session.query(db.func.max(Images.id)).scalar()
        filename = str(max_id + 1) + '.gif'
        url_file_path = UPLOAD_FOLDER+'/' + str(max_id + 1) + '.gif'
        temp_file_name = str(max_id + 1)
        with open(url_file_path, 'wb') as f:
            print remote
            f.write(remote.content)

    insert_data(image_form_data.get('Image Title'), image_form_data.get('Description'), LINK_FOLDER+temp_file_name,
                image_form_data.get('Image Tag'), image_form_data.get('Category'), session['user'])

    path = UPLOAD_FOLDER + "/" + filename

    converted_image = Image.open(path)
    converted_image.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_file_name+'.png'))
    print('data posted')
    image_list = get_image_data()
    print('data sending')
    return jsonify(image_list)


def get_searched_data(key):
    """
    This function is searching Images on the basis of key.
    :param key: Key to match the data.
    :return: Returns list of images whose tag, title and description contains key.
    """
    key = str(key)
    result = Images.query.filter(or_(Images.title.contains(key), Images.tag.contains(key),
                                     Images.description.contains(key))).all()
    image_list = []
    for row in result:
        image_list.append(row.serialize(session['user']))
    return image_list


def get_category_data(key):
    """
    Searching Images on the basis of category.
    :param key: Category
    :return: Returns list of images whose category matches key.
    """
    key = str(key.strip())
    if key != "All":
        result = Images.query.filter_by(category=key).all()
    else:
        result = Images.query.order_by(desc(Images.id)).all()
    image_list = []
    for row in result:
        image_list.append(row.serialize(session['user']))
    return image_list


@app.route('/search', methods=['GET'])
def search():
    """
    Search route
    """
    key = request.args.get('key')
    result = get_searched_data(key)
    return jsonify(result)


@app.route('/category', methods=['GET'])
def category_search():
    """
    Search category route
    """
    key = request.args.get('category')
    result = get_category_data(key)
    print result
    return jsonify(result)


def email_existence(email):
    """
    This function is checking either an email exist, during signup.
    :param email: email to be checked
    """
    result = Users.query.filter_by(email=email).first()
    if result is None:
        print "No email exist"
        return True
    else:
        print "email exist"
        return False


@app.route('/email_availability/', methods=['GET'])
def email_availability():
    """
    Email availability route
    """
    email = request.args.get('email')
    print(email)
    if email_existence(str(email)) is True:
        return "true"
    else:
        return "false"


def register_user(name, password, email):
    """
    This function is registering the user.
    :param name: Name of user
    :param password: Password of user
    :param email: Email of user
    """
    name = str(name)
    password = str(password)
    email = str(email)
    new_user = Users(name=name, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()


@app.route('/login', methods=['GET'])
def login():
    """
    Login route.
    """
    return render_template("login.html")


def get_authenticated(email, password):
    """
    This function is authenticating user for Login.
    :param email: Email of user
    :param password: Password
    :return: Status of authentication.
    """
    result = Users.query.filter(and_(Users.email == str(email), Users.password == str(password))).all()
    if result.__len__() < 1:
        return False
    else:
        session['user'] = result[0].id
        return True


@app.route('/layout', methods=['GET'])
def layout():
    """
    Layout route
    :return:
    """
    if 'user' in session:
        return render_template("layout.html")
    else:
        return redirect(url_for('login'))


@app.route('/load_data', methods=['GET'])
def load_data():
    """
    Load data route. This function is loading data on layout page after loading.
    :return: Returns all images
    """
    image_list = get_image_data()
    print(image_list)
    return jsonify(image_list)


@app.route('/login/', methods=['GET'])
def authentication():
    """
    Login route for authentication
    :return: Returns Login status
    """
    result = get_authenticated(request.args.get('email'), request.args.get('password'))
    if result is True:
        print("authenticated")
        return "true"
    else:
        return "false"


@app.route('/signup', methods=['GET'])
def signup_page():
    """
    Rendering signup page.
    :return:
    """
    return render_template("signup.html")


@app.route('/signup/', methods=['POST'])
def signup():
    """
    Signup route for registration.
    """
    form_data = request.form
    register_user(form_data.get('user_name'), form_data.get('password'), form_data.get('email'))
    return redirect(url_for('login'))


def delete_image(image_id):
    """
    This function is deleting image. Accepts image id from delete route and deletes image.
    :param image_id:
    :return:
    """
    image_id = int(image_id)
    Images.query.filter(Images.id == image_id).delete()
    db.session.commit()


@app.route('/delete', methods=['GET'])
def delete():
    """
    This is delete route. To delete an image.
    :return:
    """
    image_id = request.args.get('image_id')
    delete_image(image_id)
    image_list = get_image_data()
    return jsonify(image_list)


@app.route('/edit', methods=['GET'])
def edit():
    """
    This function edit content of image.
    """
    result = Images.query.filter_by(id=int(request.args.get('image_id'))).first()
    result.description = request.args.get('text')
    db.session.commit()
    return "true"


@app.route('/logout', methods=['GET'])
def logout():
    """
    Logout route.
    :return:
    """
    if 'user' in session:
        session.pop('user', None)

    return redirect(url_for('login'))

if __name__ == '__main__':
    # init_db()
    app.run()

    app.debug = True


@app.teardown_appcontext
def close_db():
    """
    Close database at end of app context.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
