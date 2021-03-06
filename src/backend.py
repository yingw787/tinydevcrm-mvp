import os
from flask import Flask, flash, request, send_from_directory
from werkzeug.utils import secure_filename
import psycopg2
import subprocess

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv'}

# Set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='')
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def send_html():
    # See flask static_folder=''
    return app.send_static_file('frontend.html')

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

@app.route('/create-matview-refreshes-table', methods=['GET'])
def create_materialized_view_refreshes_table():
    # Run file create_matview_refreshes_table.sql
    path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'create_matview_refreshes_table.sql'
    ))

    subprocess.call(f'PGPASSWORD=postgres psql -U postgres -d postgres -af {path}', shell=True)

    return "Table should be created properly."

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
    # It stopped again. You can see the logs for services registered uing
    # systemctl using command: 'journalctl -u postgresql'
    #
    psql_conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
    psql_cursor = psql_conn.cursor()

    cron_pid = None

    if request.method == 'GET':
        # Handle duplicates and what not later, just get it in
        psql_cursor.execute("SELECT cron.schedule('* * * * *', 'REFRESH MATERIALIZED VIEW mat_view')")
        psql_conn.commit()

        psql_cursor.execute("SELECT cron.schedule('* * * * *', 'INSERT INTO matview_refresh_events(matview_name, status, status_change_time) VALUES (''mat_view'', ''new'', NOW())')")
        psql_conn.commit()
        cron_pid = psql_cursor.fetchone()[0]

        # I think https://stackoverflow.com/a/44657411/1497211 has to take place
        # after table cron.job takes place
        psql_cursor.execute("UPDATE cron.job SET nodename=''")
        psql_conn.commit()

    psql_cursor.close()
    psql_conn.close()

    return f'Successfully scheduled job with pg_cron on database "postgres". Cron PID should be {cron_pid}.'

# TODO: pub/sub channel to notify services about materialized view refresh
#
# Woah there's not only PL/pgSQL but also PL/Python (though its completely
# untrusted so anybody can do everything)
#
# There's both plpythonu2 and plpythonu3
@app.route('/publish-mat-view-changes-to-channel', methods=['GET'])
def publish_materialized_view_changes_to_channel():
    # Created file trigger_on_mat_view_refresh.sql
    #
    # I think this may have to be run as part of shutils or subprocess
    # shell=True, but I don't think it can be run as part of psycopg2 since it's
    # partially procedural and not pure SQL.
    #
    # Having problems with postgres authentication via the command line. This is
    # due to configuration with pg_hba.conf.
    #
    # https://stackoverflow.com/a/18664239/1497211
    #
    # Update user 'postgres' from 'peer' to 'md5'.
    #
    # Restarted PostgreSQL database, and I think cron job will persist because
    # it is stored as part of table 'cron.job'; \c postgres or relevant database
    # after logging in.
    #
    # I don't think you can fire a trigger based on a materialized view refresh
    # event...I think you need to probably modify the job scheduler in order to
    # insert a value into a matview_refresh_view table and then send an event
    # based on an update of a concrete table.
    #
    # The nice thing about that is that you can also get "logging" for free as
    # well.
    #
    # I wonder whether you can auto limit the size of the table as a rolling
    # window, so that way you don't use too much disk. I think this should be
    # possible since you can create triggers based on updates only, and deletes
    # / inserts count as their own thing.
    #
    # AGH cron stopped working
    #
    # See blog post about how to set destination for PostgreSQL logs:
    # https://www.endpoint.com/blog/2014/11/12/dear-postgresql-where-are-my-logs
    #
    # I'll probably only do this for the MVP, not for this proof of concept.
    psql_conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
    psql_cursor = psql_conn.cursor()

    if request.method == 'GET':
        # Run trigger_on_mat_view_refresh.sql
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'trigger_on_mat_view_refresh.sql'
        ))
        subprocess.call(f'PGPASSWORD=postgres psql -U postgres -d postgres -af {path}', shell=True)

    psql_cursor.close()
    psql_conn.close()

    return "Set trigger to publish materialized view changes to channel."

if __name__=="__main__":
    app.run()
