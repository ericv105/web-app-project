from flask import Blueprint, render_template, request, redirect, current_app, flash
from flask_login import login_required, current_user
import os
from .models import Upload

"""
This file requires users to be logged in before they can send an image to the server.
The data sent will contain the username, filename, and contents of the file.
The upload will fail if the user does not send an image of extension type jpg/jpeg or png.

When the image is successfully sent from the client to the server, the server will discard the original filename.
The filename is then named an arbitrary name generated by a UID function.
This UID along with the username will be stored into a database with present up/down votes.

Example data structure of image uploaded
{
    "Filename": "1234567890.png"
    "Username": "Bob"
    "Upvotes": 0
    "Downvotes": 0
}
"""


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
uploads = Blueprint('uploads', __name__)


def validate_file(filename):
    # Checks if the filename has a '.' and checks whether the extension is allowed
    # Returns a boolean value
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rc(len):
    # Generate a random string of given length
    return os.urandom(len).hex()[len:]

def generateUID():
    # Generate a UID
    return "{}-{}-{}".format(rc(5),rc(8),rc(5))


# login_required decorator is used to prevent unauthenticated users from accessing the home page.
@uploads.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:
            image = request.files["image"]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if image.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # discard the filename and generate a random UID as the filename for the file
            if image and validate_file(image.filename):
                ext = image.filename.rsplit(".", 1)[1]
                filename = generateUID() + "." + ext
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(os.path.join(current_app.root_path, file_path))
                new_upload = Upload(
                    filename=filename,
                    votes=0,
                    file_path=file_path
                ).save()
                print("Saved image: {}".format(filename))
            return redirect('/')

    return render_template('upload.html', user=current_user)
