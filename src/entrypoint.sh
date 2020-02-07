#!/bin/sh
#
# Script to run after Docker build process has completed and runtime
# configuration begins.

# Start the PostgreSQL database.
#
# Need to start with '&' because otherwise postgresql will shut down after bash
# script completes (?). Cannot script into Dockerfile.
service postgresql start &

# Start the Flask backend server.
python3 /app/backend.py &

# Keep the container running.
tail -f /dev/null
