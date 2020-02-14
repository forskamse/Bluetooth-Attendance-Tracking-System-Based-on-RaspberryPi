#!/bin/bash
cd /var/lib/grafana/plugins/grafana-image-renderer/
node build/app.js server --port=8081 &
cd /path/to/your/Project
sudo python3 RPi-Bluetooth-Attendance-Information-Collection-System.py &