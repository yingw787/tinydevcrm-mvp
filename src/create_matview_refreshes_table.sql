-- Creates a table to store events where the job scheduler refreshes a certain
-- materialized view.
--
-- TODO: See whether there's a way in order to restrict the number of

CREATE TYPE matview_refresh_event_status AS ENUM ('new', 'sent')

DROP TABLE IF EXISTS matview_refresh_events;

CREATE TABLE matview_refresh_events(
    id SERIAL,
    matview_name varchar(256),
    status matview_refresh_event_status,
    status_change_time timestamp
);
