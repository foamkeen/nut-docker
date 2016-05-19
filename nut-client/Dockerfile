FROM resin/rpi-raspbian:jessie
RUN apt-get update && apt-get install -y nut-client python3-pip
RUN pip3 install influxdb
COPY ups_influxdb.py ups_influxdb.py
ENTRYPOINT ["/ups_influxdb.py"]
