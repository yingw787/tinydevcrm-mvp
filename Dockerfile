# Docker image to wrap everything in one "environment".

FROM ubuntu:18.04

RUN apt-get -y update
RUN apt-get -y upgrade
