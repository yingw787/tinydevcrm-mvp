-- Create a trigger on materialized view refresh
--
-- Hopefully I can run this file using Python / shutil if not Python / psycopg2
--
-- Inspired by: https://layerci.com/blog/postgres-is-the-answer/
CREATE OR REPLACE FUNCTION materialized_view_refresh_notify()
    RETURNS trigger AS
$$
BEGIN
    PERFORM pg_notify('matview_refresh_channel', NEW.id::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER matview_refresh
    AFTER INSERT OR UPDATE OF status
    ON matview_refresh_events
    FOR EACH ROW
EXECUTE PROCEDURE materialized_view_refresh_notify();
