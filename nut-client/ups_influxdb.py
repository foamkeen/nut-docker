#!/usr/bin/env python
import subprocess
import time
from influxdb import InfluxDBClient

influxdbhost = 'influxdb'
upsdhost = 'upsd'
upsname = 'sua1000i'

ups = {}

while True:
    for ln in subprocess.check_output(['upsc', upsname + '@' + upsdhost]).split('\n'):
        if ln: data = ln.split(': ')
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
    client = InfluxDBClient(influxdbhost, 8086, 'admin', 'admin', 'ups')
    client.write_points(body)
    time.sleep(5)