import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file part!"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return "No selected file!"
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)

            persist_filename = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
            file.save(persist_filename)
            return f"Saved file to '{persist_filename}' successfully!"

    return "Upload route with GET request!"

if __name__=="__main__":
    app.run()
