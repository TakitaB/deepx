
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'



class UploadImage(FlaskForm):
    file = FileField()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """uploads an image"""
    form = UploadImage()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return "<h1> Insert Neural Network Magic....  <h1>"

    return render_template("index.html",form=form)


if __name__ == '__main__':
    app.run(debug=True)
