#!/usr/bin/env python3
"""Backend.
"""

import os

from flask import request
from flask import redirect
from flask import Flask

from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FILE = '/tmp'
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FILE
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def hello_world():
    print("Hit endpoint '/'.")
    return "Hello, World!"

@app.route('/upload-file', methods=['POST'])
def upload_file():
    print("Hit endpoint '/upload-file'.")

    import ipdb
    ipdb.set_trace()

    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            print('No file selected for uploading')
            return redirect('/')

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FILE'], filename))
        print('File successfully uploaded')
        return redirect('/')

if __name__=="__main__":
    os.environ["FLASK_APP"] = "backend.py"
    app.run(port=5000)
