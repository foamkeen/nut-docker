FROM resin/rpi-raspbian:jessie
RUN apt-get update && apt-get -y install nut-server
COPY nut.conf ups* /etc/nut/
RUN chgrp nut /etc/nut/*
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 3493
