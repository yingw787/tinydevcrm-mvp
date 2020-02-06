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

        psql_cursor.execute('SELECT * FROM mat_view;')
        result = psql_cursor.fetchall()

        print(f'Result of psql cursor SELECT * FROM mat_view: {result}')

    psql_cursor.close()
    psql_conn.close()

    return "Successfully create materialized view 'mat_view' in PostgreSQL database 'postgres' and table 'postgres'."

@app.route('/refresh-materialized-view', methods=['GET'])
def refresh_materialized_view():
    psql_conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
    psql_cursor = psql_conn.cursor()

    if request.method == 'GET':
        psql_cursor.execute('SELECT * FROM mat_view;')
        result = psql_cursor.fetchall()

        print('Refreshing materialized view.')
        print(f'Materialized view before refresh: {result}')

        psql_cursor.execute('REFRESH MATERIALIZED VIEW mat_view;')
        psql_conn.commit()

        print('Materialized view refreshed.')

        psql_cursor.execute('SELECT * FROM mat_view;')
        result = psql_cursor.fetchall()

        print(f'Materialized view after refresh: {result}')

    psql_cursor.close()
    psql_conn.close()

    return "Materialized view should be refreshed."

@app.route('/register-view-with-job-scheduler', methods=['GET'])
def setup_job_scheduler_for_materialized_view():
    # Use pg_cron to refresh all materialized views on a per-minute granularity

    # NOTE: pgCron is a global thing, I don't think it's appropriate to expose
    # that via an endpoint, need to Dockerize this in order to script pg cron
    # setup.

    # Apparently pg_cron package archive may only be for PostgreSQL 11; need to
    # build myself in order to use PostgreSQL 12.
    #
    # Git clone source.
    #
    # Need to change path because I'm not using PostgreSQL 11.
    # export PATH=/usr/lib/postgresql/12/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    #
    # Then I need to install postgresql-server-dev-NN for building a service-side extension.
    # sudo apt-get install -y postgresql-server-dev-12
    #
    # make && sudo PATH=$PATH make install
    #
    # Got the problem of not setting conf parameters:
    #
    # yingw787=# CREATE EXTENSION pg_cron;
    # ERROR:  unrecognized configuration parameter "cron.database_name"
    # CONTEXT:  PL/pgSQL function inline_code_block line 3 at IF
    # yingw787=#
    #
    # I need to edit the conf file:
    #
    # yingw787=# SHOW config_file;
    #                config_file
    # -----------------------------------------
    #  /etc/postgresql/12/main/postgresql.conf
    # (1 row)
    #
    # yingw787=#
    #
    # It WORKS
    #
    # OH MY GOODNESS AWS RDS doesn't allow you to install your own PostgreSQL
    # extensions...it looks like I probably have to package all of this as an
    # EC2 instance or a Docker thing for final deployment after all...
    #
    # Do 'SELECT * FROM cron.job' in order to see the full list of cron jobs
    #
    # Hmm, cron job doesn't seem to be running; make sure that it has auth for
    # user running the cron job
    #
    # https://stackoverflow.com/a/44657411/1497211
    #
    # Find the hba_file using PostgreSQL, because users can place it anywhere
    #
    # SHOW hba_file; /etc/postgresql/12/main/pg_hba.conf
    #
    # Added to hba file 'local all yingw787 peer'
    #
    # Then I ran "UPDATE cron.job SET nodename = '';"
    #
    # Then I added "SELECT cron.schedule('* * * * *', 'SELECT 1');"
    #
    # It appears after all this the cron is updating successfully!!
    #
    psql_conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
    psql_cursor = psql_conn.cursor()

    cron_pid = None

    if request.method == 'GET':
        # Handle duplicates and what not later, just get it in
        psql_cursor.execute("SELECT cron.schedule('* * * * *', 'REFRESH MATERIALIZED VIEW mat_view');")
        psql_conn.commit()

        cron_pid = psql_cursor.fetchone()[0]

    psql_cursor.close()
    psql_conn.close()

    return f'Successfully scheduled job with pg_cron on database "postgres". Cron PID should be {cron_pid}.'

# TODO: pub/sub channel to notify services about materialized view refresh


if __name__=="__main__":
    app.run()
