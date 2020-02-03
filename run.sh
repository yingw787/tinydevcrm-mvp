#!/bin/sh
#
# Shell script for building and configuring the complete environment for
# `tinydevcrm-mvp`.
#
# Assumptions:
#   - `docker` is installed and available as $(which docker)
#   - `git` is installed and available as $(which git)

DOCKER=$(which docker)
GIT=$(which git)
