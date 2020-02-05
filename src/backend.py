import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import psycopg2

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

@app.route('/save-csv-to-db', methods=['GET'])
def save_csv_to_db():
    psql_conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432)
    psql_cursor = psql_conn.cursor()

    # Saves persisted CSV file '/tmp/sample.csv' to PostgreSQL.
    if request.method == 'GET':
        psql_cursor.execute('DROP TABLE IF EXISTS sample; CREATE TABLE sample ("SomeNumber" INTEGER, "SomeString" VARCHAR);')
        psql_conn.commit()

        sqlstr = "COPY sample FROM STDIN DELIMITER ',' CSV HEADER"

        with open('/tmp/sample.csv') as f:
            psql_cursor.copy_expert(sqlstr, f)
        psql_conn.commit()

    psql_cursor.close()
    psql_conn.close()

    return "Successfully inserted CSV file '/tmp/sample.csv' to PostgreSQL table 'sample'."

@app.route('/create-materialized-view', methods=['GET'])
def create_materialized_view():
    # This is a psql random number generator; it takes fractional seconds, so
    # the values should change faster than a materialized view can refresh.
    #
    # SELECT CAST( EXTRACT(SECOND FROM NOW()) * 1000000 AS INTEGER) % 10

    # SELECT * FROM sample WHERE "SomeNumber" = CAST( EXTRACT(SECOND FROM NOW()) * 1000000 AS INTEGER) % 10;

    psql_conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432)
    psql_cursor = psql_conn.cursor()

    if request.method == 'GET':
        psql_cursor.execute('DROP MATERIALIZED VIEW IF EXISTS mat_view;')
        psql_cursor.execute('CREATE MATERIALIZED VIEW mat_view AS SELECT * FROM sample WHERE "SomeNumber" = CAST( EXTRACT( SECOND FROM NOW()) * 1000000 AS INTEGER) % 10;')
        psql_conn.commit()

    psql_cursor.close()
    psql_conn.close()

    return "Successfully create materialized view 'mat_view' in PostgreSQL database 'postgres' and table 'postgres'."


if __name__=="__main__":
    app.run()
