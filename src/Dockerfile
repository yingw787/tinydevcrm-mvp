# Docker image to wrap everything in one "environment".

FROM ubuntu:18.04

# Configure environment variables for Docker build process.
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

# Install dependencies necessary for installing other dependencies.
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN apt-get install -y ca-certificates
RUN apt-get install -y gnupg
RUN apt-get install -y lsb-core

# Install PostgreSQL 12.x from PostgreSQL .deb package archive. Note that as of
# February 3rd, 2020, the Ubuntu default package archive contains PostgreSQL
# 10.x, so floating versioning will not work even for the MVP.

# Disable warning "Warning: apt-key output should not be parsed (stdout is not a
# terminal)" according to: https://stackoverflow.com/a/49462622
RUN curl -sSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 apt-key add -

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list

# Installing PostgreSQL from scratch involves configuring tzdata.
# Non-interactive method of configuring tzdata comes from this ServerFault
# answer: https://serverfault.com/a/846989
#
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN apt-get install -y tzdata
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get -y update
RUN apt-get install -y postgresql-12
RUN apt-get install -y postgresql-client-12
RUN apt-get install -y postgresql-contrib-12

ENTRYPOINT [ "/app/entrypoint.sh" ]
