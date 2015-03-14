FROM debian:7.8

MAINTAINER David Url <david@x00.at>

# set environment for apt
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

# install stuff
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y tar nano wget telnet netcat

# install dependencies
RUN apt-get install -y python python-dev python-pip
RUN apt-get install -y nginx supervisor

RUN pip install uwsgi Flask pandas

ADD ./dist/smartmeter-analyze /application

EXPOSE 5000
WORKDIR /application
CMD ["/usr/bin/python", "smutil", "run_webutil"]
