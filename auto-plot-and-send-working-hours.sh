#!/bin/bash

cd /home/pi/projects/
/home/pi/.virtualenvs/bt/bin/python /home/pi/projects/plot-working-hours.py
sendEmail -f sender_email_address -t receiver_email_address -u "Working Hours from RaspberryPi" -m "Working hours of $(date --date '1 days ago' +%Y-%m-%d)" -a /home/pi/projects/working-hours.png -s sender_email_smtp_server_address  -o tls=yes -xu sender_email_address -xp sender_email_password
