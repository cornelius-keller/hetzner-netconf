FROM python:2.7.11-alpine
MAINTAINER cke@marketlogicsoftware.com

RUN apk add --update alpine-sdk linux-headers
RUN pip install netifaces==0.10.4 netaddr==0.7.18

ADD set_routes.py /set_routes.py
RUN chmod +x /set_routes.py

ADD restore_routes /etc/network/if-post-up.d/restore_routes
RUN chmod +x /etc/network/if-post-up.d/restore_routes

ENTRYPOINT  /set_routes.py
