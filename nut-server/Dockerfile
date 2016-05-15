FROM resin/rpi-raspbian
RUN apt-get update && apt-get install nut
COPY nut.conf ups* /etc/nut/
RUN chgrp nut /etc/nut/*
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 3493
