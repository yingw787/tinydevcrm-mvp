-- Creates a table to store events where the job scheduler refreshes a certain
-- materialized view.
--
-- TODO: See whether there's a way in order to restrict the number of records
-- stored, in order to avoid out of disk space errors because of constant event
-- generation. I think shouldn't affect trigger definition or creation because
-- you can make triggers that target update statements only, and deletion of
-- records shouldn't be the same as updating. Need to explore this.

CREATE TYPE matview_refresh_event_status AS ENUM ('new', 'sent');

DROP TABLE IF EXISTS matview_refresh_events;

CREATE TABLE matview_refresh_events(
    id SERIAL,
    matview_name varchar(256),
    status matview_refresh_event_status,
    status_change_time timestamp
);
