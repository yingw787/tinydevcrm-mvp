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

-   The 'pg_cron' project by Citus Data only publishes packages for PostgreSQL
    11.x, not PostgreSQL 12.x. In order to support PostgreSQL 12.x, I needed to
    build the project from source myself. This wasn't difficult at all, but it
    underlines how different open-source projects march to the beat of their own
    drums, and you the core developer must remain ready to create your own build
    pipeline.
