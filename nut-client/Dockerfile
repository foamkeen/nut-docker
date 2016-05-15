FROM resin/rpi-raspbian:jessie
RUN apt-get update && apt-get install -y nut-client python-pip
RUN pip install influxdb
COPY ups_influxdb.py ups_influxdb.py
ENTRYPOINT ./ups_influxdb.py 2> /dev/null
