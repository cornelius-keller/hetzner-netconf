FROM python:2.7.11-alpine
MAINTAINER cke@marketlogicsoftware.com

RUN apk add --update alpine-sdk linux-headers
RUN pip install netifaces==0.10.4 netaddr==0.7.18

ENV IFACE=enp0s31f6

ADD set_routes.py /set_routes.py
RUN chmod +x /set_routes.py

ENTRYPOINT  /set_routes.py
