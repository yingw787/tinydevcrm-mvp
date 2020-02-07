#!/usr/bin/env python3

# Subscribe to channel using gist: https://gist.github.com/quiver/4240546

# subscriber of pub/sub pattern
# Usage:
# $ python sub.py <channel> <channel> ...
# http://initd.org/psycopg/docs/advanced.html#asynchronous-notifications

import select
import sys

import psycopg2
import psycopg2.extensions

DSN = "dbname=postgres user=postgres"
conn = psycopg2.connect(DSN)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()

for channel in sys.argv[1:]:
    print('SUBSCRIBE TO channel #%s' % channel)
    curs.execute("LISTEN %s;" % channel)

epoll = select.epoll()
epoll.register(conn, select.EPOLLIN)

while True:
    try:
        events = epoll.poll()
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop()
            print("#%s - %s" % (notify.channel, notify.payload))
    except (BaseException, err):
        print(err)
        break

for channel in sys.argv[1:]:
    print('UNSUBSCRIBE FROM channel #%s' % channel)
    curs.execute("UNLISTEN %s;" % channel)
