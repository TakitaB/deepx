
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["MAX_CONTENT_LENGTH"] = 4*1024*1024 #4MB max-limit



class UploadImage(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg'], 'Images only!')]) #allow only files with the jpg extension to be submitted


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """uploads an image"""
    form = UploadImage()

    #if client attempts to submit the form (ie sends a POST request)
    if request.method =="POST":

        #first check to see if there are any files in the "uplaod" folder. If the folder is not empty,
        # delete any files that are in it: the "upload" directory it functions as a temp dir, and we
        # only want the one image the client  # uplaods to the server to ever be there)


        if len(os.listdir("uploads")) != 0:
            for f in  os.listdir("uploads"):
                path_to_file = os.path.join("uploads", f)
                os.remove(path_to_file)


        #check if the file  the client wants to upload matches the specified requirements
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            form.file.data.save('uploads/' + filename) #grab the file and save it in the uploads directory
            flash("Image uploaded successfully.")
            return render_template("index.html",form=form, filename=filename)
        else:
            #else flash a message to the client telling them that the upload was rejected

            flash("Allowed image types are only jpgs")
            return redirect(url_for('upload'))

    #else just return the page if client submits a GET request (ie just requests the page to the server)
    return render_template("index.html",form=form)


if __name__ == '__main__':
    app.run(debug=True)
