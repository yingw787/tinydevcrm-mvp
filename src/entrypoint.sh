#!/bin/sh
#
# Script to run after Docker build process has completed and runtime
# configuration begins.

# Start, then configure, PostgreSQL.
service postgresql start

# Start the Flask backend server.
python3 /app/backend.py &

# Keep the container running.
tail -f /dev/null
