#!/bin/bash
set -e

chgrp nut /dev/bus/usb/*/*
upsdrvctl start
exec upsd -D
