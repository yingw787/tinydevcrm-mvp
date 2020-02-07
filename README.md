# `tinydevcrm-mvp`: Proof of concept for the TinyDevCRM project.

## Overview

This is a proof of concept for [TinyDevCRM](https://tinydevcrm.com).

Originally, this was intended to be a minimal viable product (MVP), but since
the technical merits of the project still needed to be proved out, I decided to
use this purely as a technical learning exercise. I don't want to change the
name of the project in case changing the URI will break unknown backlinks.

## Requirements

1.  Upload a CSV file via a webpage, using a button and a file selector. The
    specific test CSV consists of one column, with header "AColumnOfNumbers",
    with ten records, values 0 through 9.

2.  Upon file upload, send the file data to API endpoint `/upload-file` that
    will read the CSV file, create a PostgreSQL table based on the data, and
    load it into a PostgreSQL table.

3.  Create a materialized view on the loaded data, installing any and all
    dependencies or extensions necessary to do so. The specific test
    materialized view will be a `SELECT *` blanket SQL query that matches
    against the last digit of the current second.

4.  Create a materialized view refresher that will refresh the materialized view
    every so often, frequently enough to test with. Install any and all
    dependencies and extensions necessary to do so.

5.  Find a way to send an event to an external process (e.g. the Python process)
    if the materialized view is not empty. Once the event is sent, the process
    should log some amount of debug output.

That should be the *full* scope of the project. I do not currently foresee any
scope increase necessary to satisfy the requirements detailed on the [TinyDevCRM
"Coming Soon" page](https://github.com/yingw787/tinydevcrm-comingsoon).

## What This Project Is

-   **Work out basic interface contracts**: For example, currently I have the
    question of whether I could get away with two UNIX processes on the
    server-side (the Python process and the PostgreSQL process), or whether I
    would need to have more processes in order to handle event generation and
    event handling (like a `redis` or `celery` process). Having fewer processes
    may be a strict improvement to the number of deployment environments I can
    support in the future. Another question I have is whether I need to use a
    pub/sub architecture to enable clients to listen to events as they're
    generated, or whether it's possible to send all events through one process.
    I am concerned that pub/sub will use too many UNIX sockets and may pose a
    performance / memory burden if native authentication is implemented and
    multiple users are sending events.

-   **Work out opportunistic heuristics**: As I'm building this with the
    intention of using it as a platform, heuristics such as "Platformed
    applications should absolutely not need to have any specific server-side
    processes" should be written down into the 0.x release README.

## What This Project Is Not

-   **Maintainable**: After the critical pipeline is fleshed out, work will
    immediately commence on building out maintainable 0.x releases of both the
    front-end application and the back-end API, as well as scripts to maintain
    the PostgreSQL database.

-   **Uses best practices**: This project will *not* apply things like
    user authentication, testing, deployment, strict or non-strict loading of
    data, UI/UX workflow, or other kinds of best practices. I'm just getting
    something working.

## Installation & Getting Started

```bash
$ git clone \
    https://github.com/yingw787/tinydevcrm-mvp.git \
    /path/to/tinydevcrm-mvp

$ cd tinydevcrm-mvp

$ . ./src/run.sh

$ docker exec -it tinydevcrm-mvp bash

# Go to localhost:5000, submit CSV file
# 'src/sample.csv', and click every button on the page
# in order from top to bottom.

# Inside Docker container
$ python3 /app/sub.py matview_refresh_channel

# You should see the IDs of new rows added to table
# 'matview_refresh_events' in database 'postgres'
# every minute.
```

## Lessons Learned

This was a tremendous learning experience for me. Here's some of the things I
picked up:

-   The frontend is *extremely* basic. It's literally just a cascade of buttons
    detailing the workflow. I copied this from [W3School's tutorial on
    multipart/form-data](https://www.w3schools.com/TAGs/tryit.asp?filename=tryhtml_form_enctype).
    It offended my sensibilities as a former full-stack engineer to have
    something so basic, but I'm really happy I was able to practice pioneering
    and got something out the door. On top of that, the HTML file is pretty
    parseable and intuitive, which lends well to a high signal-to-noise ratio,
    and details the workflow from start to finish graphically and interactively,
    which is what I need in order to begin work on the MVP.

-   I found it difficult to iterate without having a dev server for the
    frontend. I'm guessing this is what makes things like `webpack-dev-server`
    so attractive. I don't want to include JavaScript at this stage of
    development, so I used the Flask API `app.send_static_file()` in order to
    send the HTML static file as the root route. Then, you can update the HTML
    document and refresh the page, which leads to the updated document. It's
    kind of like a dev server. On top of that, your frontend and your backend
    are at the same URL, no `file://` searching, which makes it nice for
    deployments because you know where all your assets are.

    Forking static files is something that I might consider for the final
    project, but I'm honestly leaning towards building a server-side rendered
    static bundle at the moment. IMHO, having the backend server send files is
    much less efficient than using a CDN, and it's just more work that might
    result lead the server to crash given high enough load to resources. Also,
    it's not great separation of concerns; despite it all I'd rather build a
    bundle and edit the assets if I need to change them, rather than use Jinja
    and potentially be limited by the given DSL.

-   I wasn't familiar with HTTP POST requests. This proof of concept uses a bare
    HTML document to submit files to the backend API. After sending the file to
    the backend API, *the file will exist on the backend server*. I had thought
    there would be a way to reference the file in memory without having to save
    it, like Flask would have a `FileDescriptor` object or something. I don't
    think that's the case. This isn't a huge deal to me; since the file is a
    transient state to the PostgreSQL table anyways, I need to load the file
    from `/tmp` or wherever I had set `app.config['UPLOAD_FOLDER']` to be to a
    PostgreSQL table, and then immediately delete the uploaded file. This way, I
    shouldn't have to deal with blob storage, and ideally I can keep disk space
    available for the database itself.

-   I still find the fact that `psycopg2` doesn't have context management for
    its PostgreSQL connection and cursor frustrating. I don't understand the
    intricacies of the project, but I'm not sure why it's so hard to implement
    `__enter__` and `__exit__`. I am worried about what might happen if there
    are a bunch of dangling PostgreSQL connections due to poor error handling
    over a long period of time. I'll need to keep an eye out for this, and
    ensure that I keep the number of concurrent connections down to a minimum,
    and maybe some way in order to notify me of dangling connections.

-   I'm not sure whether the RFC-4180 compliant CSV parser will be a thing.
    Ideally, I would want a POSIX-compatible tool to translate CSV files into
    Parquet files, since Parquet files have a highly structured schema and
    they're a framework-agnostic binary format. I trust Parquet much more and
    that others can put together a fully-featured and correct Parquet parser
    than a CSV parser. Right now, the PostgreSQL `COPY sample FROM STDIN` works
    fine and I have larger concerns in working towards feature parity.

-   The 'pg_cron' project by Citus Data only publishes packages for PostgreSQL
    11.x, not PostgreSQL 12.x. In order to support PostgreSQL 12.x, I needed to
    build the project from source myself. This wasn't difficult at all, but it
    underlines how different open-source projects march to the beat of their own
    drums, and you the core developer must remain ready to create your own build
    pipeline.

-   You can't attach a PostgreSQL trigger based onto a refresh materialized view
    command directly. The [example blog post I
    referenced](https://layerci.com/blog/postgres-is-the-answer/) when creating
    this trigger inserts events into a PostgreSQL table, then creates a trigger
    from every new row that has a particular status (like "new"). This concerns
    me in that there's a constantly growing table that the database needs to
    vaccum every so often. On the plus side, a log of events would really help
    in terms of understanding the job scheduler.

-   Log management in PostgreSQL is a big unknown to me. Cron job failures were
    common during development, and I'm still not sure whether I need to call
    `UPDATE cron.job SET nodename=''` after every `INSERT` statement into
    `cron.job`. I need some way in order to extricate those logs and make them
    visible to admin-level users; otherwise debugging cron job failures will be
    quite a pain.

-   There's not only PL/pgSQL, but also PL/Python as `LANGUAGE plpythonu`.
    There's Python 2 and Python 3 versions of this procedural extension. I
    didn't know this existed. The type translation is documented, but I don't
    know how much I like it (e.g. `'f'` I think translates to `True` in Python
    because it's not an empty string; however I believe this is `'False'` in
    PL/pgSQL).

-   I'm not sure how `pg_hba.conf` authentication levels like `md5` and `peer`
    work. I need to read through the docs for this.

-   I'm not sure how I might make all of this infrastructure stand up
    dynamically. How would I save config changes?

-   I'm not sure how pieces of this application are coupled together. I think
    initially, a change that would break say a materialized view (maybe a SQL
    migration) would simply drop the materialized view entirely. Later on, I
    might recreate the materialized view automatically and ask the user whether
    it's fine.

-   I still want to stick to a princple of "done"-ness, and be able to entirely
    down the build chain for this project as soon as possible.

-   I'm elated that the job scheduler can reference all materialized views, and
    that only one pub/sub channel is necessary in order to send events. The cron
    job description and scheduling is how the frequency of job runs and what
    aspects of data are touched by the job scheduler, and subscribers to the
    pub/sub channel can disambiguate messages and send them to the right user or
    service, which means permissioning can stay in hardcoded source code. This
    should mean that only a minimal number of processes and sockets need to be
    open at any time, rather than scaling linearly with the number of users
    (which is something I feared). It also means permissioning shouldn't be too
    hard. I did envision giving every year their own PostgreSQL user (properly
    permissioned) in order for them to access their own data, views, and
    triggers without compromising everybody else. It seems like this is possible
    even with the current setup, or at least I see a path forward.
