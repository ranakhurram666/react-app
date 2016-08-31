"""
This module contains server side flask coding.
"""
# Builtin Imports
import os
# 3rd party imports
from flask import Flask, request, session, g, redirect, url_for, \
     render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from PilLite import Image
import requests
import requests.packages.urllib3
# Importing self made Model classes
from db import db, Images
requests.packages.urllib3.disable_warnings()


UPLOAD_FOLDER = 'static/css/img'
LINK_FOLDER = '../static/css/img/'


def init_app():
    apps = Flask(__name__)
    apps.config.from_object(__name__)
    apps.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    apps.secret_key = "secret key"
    CORS(apps)
    # db.create_all()
    return apps

app = init_app()


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    """
    This function is uploading image to sever and storing its object in database. In this function Image is
    converted in to .png by extracting 1st frame of original image. For given urls of images, image is downloaded from
    url and converted into .png
    :return: This function return list of all images objects after uploading image
    :rtype: List of Image objects
    """

    image_form_data = request.form
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
        url_file_path = UPLOAD_FOLDER + '/' + str(max_id + 1) + '.gif'
        temp_file_name = str(max_id + 1)
        with open(url_file_path, 'wb') as f:

            f.write(remote.content)

    message = Images.insert_data(image_form_data.get('Image Title'), image_form_data.get('Description'),
                       LINK_FOLDER+temp_file_name, image_form_data.get('Image Tag'), image_form_data.get('Category'),
                       session['user'])
    if message == "error":
        return message
    path = UPLOAD_FOLDER + "/" + filename

    converted_image = Image.open(path)
    converted_image.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_file_name+'.png'))

    image_list = Images.get_image_data()

    return jsonify(image_list)


@app.route('/search', methods=['GET'])
def search():
    """
    This endpoint search images on the basis of key words.
    :return: Returns List of Images
    :rtype: Images
    """
    key = request.args.get('key')
    result = Images.get_searched_data(key)
    if result == "error":
        return result
    return jsonify(result)


@app.route('/category', methods=['GET'])
def category_search():
    """
    This endpoint search images on the basis of category.
    :return: Returns List of Images
    :rtype: Images
    """
    key = request.args.get('category')
    result = Images.get_category_data(key)
    if result == "error":
        return result
    return jsonify(result)


@app.route('/email_availability', methods=['GET'])
def email_availability():
    """
    This endpoint is checking email availability for signup purpose.
    :return: Returns status of availability
    :rtype: str
    """
    email = request.args.get('email')
    result = Images.email_existence(str(email))
    if result == "error":
        return result
    if result:
        return "true"
    else:
        return "false"


@app.route('/redirect_to_login', methods=['GET'])
def login():
    """
    This endpoint renders login page when user wants to login and clicks on login button
    """
    return render_template("login.html")


@app.route('/layout', methods=['GET'])
def layout():
    """
    Layout route
    """
    if 'user' in session:
        return render_template("layout.html")
    else:
        return redirect(url_for('login'))


@app.route('/load_data', methods=['GET'])
def load_data():
    """
    This endpoint returns list of Images when layout page is loaded for the first time..
    :return: Returns all images
    :rtype: Images
    """
    image_list = Images.get_image_data()
    if image_list == "error":
        return "error"
    return jsonify(image_list)


@app.route('/login', methods=['GET'])
def authentication():
    """
    This endpoint authenticates user login credentials e.g email and password
    :return: Returns Login status
    :rtype: str
    """
    result = Images.get_authenticated(request.args.get('email'), request.args.get('password'))
    if result == "error":
        return "error"

    if result:

        return "true"
    else:
        return "false"


@app.route('/signup', methods=['GET'])
def signup_page():
    """
    This endpoint rendering signup page when user wants to signup and clicks on register button.
    :return: render signup page
    """
    return render_template("signup.html")


@app.route('/signup/', methods=['POST'])
def signup():
    """
    This registers the user on signup
    """
    form_data = request.form
    result = Images.register_user(form_data.get('user_name'), form_data.get('password'), form_data.get('email'))
    if result == "error":
        return result
    return redirect(url_for('login'))


@app.route('/delete', methods=['GET'])
def delete():
    """
    This endpoint deletes an image.
    :return: List of images after deletion
    :rtype: Images List
    """
    image_id = request.args.get('image_id')
    Images.delete_image(image_id)
    image_list = Images.get_image_data()
    return jsonify(image_list)


@app.route('/edit', methods=['GET'])
def edit():
    """
    This route edits content of an Image
    :rtype: str
    """
    result = Images.query.filter_by(id=int(request.args.get('image_id'))).first()
    result.description = request.args.get('text')
    db.session.commit()
    return "true"


@app.route('/logout', methods=['GET'])
def logout():
    """
    This endpoint logout the user and pop the session
    """
    if 'user' in session:
        session.pop('user', None)

    return redirect(url_for('login'))



