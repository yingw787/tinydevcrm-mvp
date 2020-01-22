# `tinydevcrm-mvp`: MVP for TinyDevCRM project.

## Overview

This is a minimal viable product (MVP) for [TinyDevCRM](https://tinydevcrm.com).

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
