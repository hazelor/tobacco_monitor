#!/bin/sh
sudo echo 3 > /sys/devices/virtual/misc/gpio/mode/gpio0
sudo echo 3 > /sys/devices/virtual/misc/gpio/mode/gpio1
sudo echo 3 > /sys/devices/virtual/misc/gpio/mode/gpio2
cd /home/linaro/tobacco_monitor/terminal
sudo python main.py &
sudo ./onImgUpload.sh &


