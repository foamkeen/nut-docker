#!/usr/bin/env python

# run upsc utility with 5 seconds delay and store it's output to ups dictionary
# commit selected measurements to influxdb database using official influxdb python client

import subprocess
import time
import os
from influxdb import InfluxDBClient

# check for env variables and put defaults if not

influxdb_host = os.getenv('INFLUXDB_HOST', 'influxdb')
influxdb_name = os.getenv('INFLUXDB_NAME', 'ups')
influxdb_username = os.getenv('INFLUXDB_USERNAME', 'admin')
influxdb_password = os.getenv('INFLUXDB_PASSWORD', 'admin')
upsdhost = os.getenv('UPSD_HOST', 'upsd')
upsname = os.getenv('UPS_NAME', 'sua1000i')

ups = {}

while True:
    # upc provides lines like:
    # output.current: 0.43
    # output.frequency: 50.0
    # output.voltage: 240.4
    for upsc_line in subprocess.check_output(['upsc', upsname + '@' + upsdhost], stderr=subprocess.STDOUT).split('\n'):
        data = upsc_line.split(': ')    # so data is a list with measurement name in [0] and the value in [1]
        if len(data) == 2:  # omitting empty lines and 'Init SSL without certificate database' line, storing only 'value: data'
            ups[data[0]] = data[1]

    body = [
        {
            'measurement': 'battery',
            'fields': {
                'runtime': int(ups['battery.runtime']),
                'voltage': float(ups['battery.voltage']),
                'charge': int(ups['battery.charge']),
                'temperature': float(ups['battery.temperature'])
            }
        },
        {
            'measurement': 'load',
            'fields': {
                'percent': float(ups['ups.load'])
            }
        },
        {
            'measurement': 'current',
            'fields': {
                'amper': float(ups['output.current'])
            }
        },
        {
            'measurement': 'voltage',
            'fields': {
                'output': float(ups['output.voltage']),
                'input': float(ups['input.voltage'])
            }
        }
    ]
    client = InfluxDBClient(influxdb_host, 8086, influxdb_username, influxdb_password, influxdb_name)
    client.write_points(body)
    time.sleep(5)