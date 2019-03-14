# RaspberryPi Bluetooth Punch System Instructions

##### Clone the repository
```
cd ~
git clone https://github.com/forskamse/RaspberryPi-Bluetooth-Punch-System.git
```
##### Install dependencies and python packages
 ```
sudo apt-get install pkg-config libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev python-dev sendemail libnet-ssleay-perl libio-socket-ssl-perl
pip3 install matplotlib pandas pybluez pybluez[ble] 
```
##### Self device MAC address setting
Replace [bluetooth-punch.py - L11](https://github.com/forskamse/RaspberryPi-Bluetooth-Punch-System/blob/master/bluetooth-punch.py#L11) (if you use common device) or [bluetooth-punch.py - L12](https://github.com/forskamse/RaspberryPi-Bluetooth-Punch-System/blob/master/bluetooth-punch.py#L12) (if you use BLE device) with your device MAC address 
##### Self email setting
replace [auto-plot-and-send-working-hours.sh - L5](https://github.com/forskamse/RaspberryPi-Bluetooth-Punch-System/blob/master/auto-plot-and-send-working-hours.sh#L5) with your own receiver_email_address, sender_email_smtp_server_address, sender_email_address, and sender_email_password

##### Set boot from power on
```
sudo nano /etc/rc.local
Add the following command to /etc/rc.local before "exit 0"
/bin/bash ~/RaspberryPi-Bluetooth-Punch-System/auto-bluetooth-punch.sh
```
##### Set crontab
```
crontab -e
# Add the following command to crontab file
30 8 * * * ~/RaspberryPi-Bluetooth-Punch-System/auto-plot-and-send-working-hours.sh
```
