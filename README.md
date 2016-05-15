# nut-docker

These Dockerfiles are intended to run on Raspberry Pi, but should work as well on any x86, just replace `resin/rpi-raspbian` with `debian`

nut-server expects a UPS usb device passed to it with --device, for example:

    docker run --name upsd -d --device=$(lsusb -d 051d:0002|awk -F '[ :]' '{print "/dev/bus/usb/"$2"/"$4}') --net nut-network nut-server
You can find usb device id (051d:0002 in my case) with `lsusb`, mine APC Smart UPS 1000 reports itself like that:

    Bus 001 Device 006: ID 051d:0002 American Power Conversion Uninterruptible Power Supply
So in my case this little snippet `lsusb -d 051d:0002|awk -F '[ :]' '{print "/dev/bus/usb/"$2"/"$4}'` will transform it to `/dev/bus/usb/001/006`

nut-client contains upsc and small python script to store selected data in influxdb
