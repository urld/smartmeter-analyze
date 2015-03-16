FROM debian:7.8

MAINTAINER David Url <david@x00.at>

# set environment for apt
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

ADD ./.keys /.keys
RUN apt-key add /.keys/nginx_signing.key
RUN echo "deb http://nginx.org/packages/debian/ wheezy nginx" >> /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/debian/ wheezy nginx" >> /etc/apt/sources.list

# install stuff
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y runit
RUN apt-get install -y tar nano wget telnet netcat procps

# install dependencies:
RUN apt-get install -y python python-dev python-pip
RUN apt-get install -y nginx openssl
RUN apt-get install -y uwsgi uwsgi-plugin-python

RUN pip install Flask
RUN pip install pandas

################################################################################

# generate keys:
RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 # should be 4096
RUN openssl req -new -x509 -sha256 -newkey rsa:2048 -days 365 -nodes -out /etc/ssl/certs/nginx.pem -keyout /etc/ssl/certs/nginx.key -batch -subj "/O=David Url/CN=David Url"

# add application:
# assuming that the source distribution was already built with make
ADD ./dist/smartmeter-analyze /application

# add configuration:
RUN rm -f /etc/nginx/conf.d/default.conf
ADD ./etc /etc

# configure runit:
RUN mkdir -p /service
RUN ln -s /etc/sv/nginx /etc/service
RUN ln -s /etc/sv/nginx /service/
RUN ln -s /etc/sv/uwsgi /etc/service
RUN ln -s /etc/sv/uwsgi /service/


EXPOSE 80
EXPOSE 443
ENTRYPOINT ["runit-init"]
