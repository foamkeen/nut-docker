#!/usr/bin/env python3

# run upsc utility with 5 seconds delay and store it's output to ups dictionary
# commit selected measurements to influxdb database using official influxdb python client

import subprocess
import time
import os
import requests
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
    # upsc provides lines like:
    # output.current: 0.43
    # output.frequency: 50.0
    # output.voltage: 240.4

    p = subprocess.Popen(['upsc', upsname + '@' + upsdhost], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        # waiting 10 seconds for process to finish
        std_out, std_err = p.communicate(10)
    except TimeoutExpired:
        # killing it otherwise
        p.kill()
        std_out, std_err = p.communicate()
    std_out = std_out.decode("utf-8")
    std_err = std_err.decode("utf-8").rstrip()
    # workaround, as this line occurs on every upsc run
    if std_err != 'Init SSL without certificate database':
        print(std_err)
    # try to decode values only if 'upsc' exit code is 0
    if p.returncode == 0:
        for upsc_line in std_out.split('\n'):
            data = upsc_line.split(': ')    # so data is a list with measurement name in [0] and the value in [1]
            if len(data) == 2:  # omitting empty lines, storing only 'value: data'
                ups[data[0]] = data[1]
        try:
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
            try:
                client.write_points(body)
            except requests.exceptions.ConnectionError as e:
                # e = sys.exc_info()[0]
                print(str(e))
        except KeyError as e:
            print('Value not found: ' + str(e))
    time.sleep(5)