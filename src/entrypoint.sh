#!/bin/sh
#
# Script to run after Docker build process has completed and runtime
# configuration begins.

# Start the PostgreSQL database.
service postgresql start

# Keep the container running.
tail -f /dev/null
