#!/bin/bash

cd ~/RaspberryPi-Bluetooth-Punch-System/
python3 ~/RaspberryPi-Bluetooth-Punch-System/plot-working-hours.py
sendEmail -f sender_email_address -t receiver_email_address -u "Working Hours from RaspberryPi" -m "Working hours of $(date --date '1 days ago' +%Y-%m-%d)" -a ~/RaspberryPi-Bluetooth-Punch-System/working-hours.png -s sender_email_smtp_server_address  -o tls=yes -xu sender_email_address -xp sender_email_password
