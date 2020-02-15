
import os
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from bluetooth import discover_devices
from influxdb import InfluxDBClient
import requests.exceptions
import logging

logger = logging.getLogger("RPi Bluetooth Attendance Information Collection System")
# logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def clientRegistering(host, port, username, password_file, database):
    logger.debug("Registering InfluxDB client ...")
    password = open(password_file).read().strip()
    influx_client = InfluxDBClient(
        host=host, port=port, username=username, password=password, database=database)
    return influx_client

def msgStructuringAndWriting(influx_client, measurement, targetDevName, targetDevAddr, data):
    logger.debug("Structuring InfluxDB point ...")

    if not isinstance(data, dict):
        raise ValueError('data must be given as dict!')

    influx_msg = {
        'measurement': measurement,
        'tags': {
            'name': targetDevName,
            'address': targetDevAddr,
        },
        'fields': data
    }

    logger.debug("Writing InfluxDB point: %s", influx_msg)
    try:
        influx_client.write_points([influx_msg])
    except requests.exceptions.ConnectionError as e:
        logger.exception(e)

def targetScanning(influx_client, reg_data):
    #####################################################################################################################
    # Note that subprocess.Popen demonstrates higher reliability than os.popen in practice.
    # And with subprocess we are able to process stderr when necessary.
    #####################################################################################################################
    logger.debug("Scanning the target device ...")
    foundDevAddrs = []

    for _ in range(3): # about 20s per scanning duration; we may expect one data point per 1m
        _foundBleDevAddrs = []
        # A BLE scaning won't stop automatically, so we have to set up a timeout
        p_lescan = subprocess.Popen('timeout -s SIGINT 17s hcitool lescan',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        stdout_lescan, _ = p_lescan.communicate()
        res_lescan = stdout_lescan.decode()
        for res_line in res_lescan.strip().split('\n'):
            if 'LE Scan' not in res_line:
                devAddr = res_line.split(' ')[0]
                if devAddr.count(':') == 5:
                    _foundBleDevAddrs.append(devAddr)
        foundDevAddrs.extend(_foundBleDevAddrs)

        _foundBluetoothDevAddrs = []
        # Typically, a Bluetooth scaning will finish within 2-4s, so we don't have to set up a timeout
        p_scan = subprocess.Popen('hcitool scan',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        stdout_scan, _ = p_scan.communicate()
        res_scan = stdout_scan.decode()
        for res_line in res_scan.strip().strip('\t').split('\t'):
            if 'Scanning ...' not in res_line:
                devAddr = res_line.split(' ')[0]
                if devAddr.count(':') == 5:
                    _foundBluetoothDevAddrs.append(devAddr)
        foundDevAddrs.extend(_foundBluetoothDevAddrs)

    for targetDevName, targetDevAddr in reg_data:
        if targetDevAddr in foundDevAddrs:
            data = {'State':1}
        else:
            data = {'State':0}
        msgStructuringAndWriting(influx_client, measurement, targetDevName, targetDevAddr, data)

def dailyAlerting(influx_client, measurement, targetDevName, targetDevAddr):
    logger.debug("Triggering daily report alerting ...")
    data = {'State':2}
    msgStructuringAndWriting(influx_client, measurement, targetDevName, targetDevAddr, data)

if __name__ == "__main__":

    targetDevNames = ['Band','Phone']
    targetDevAddrs = ['C1:E3:78:ED:65:56','48:01:C5:1F:94:8C']
    
    influx_host = "127.0.0.1"
    influx_port = 8086
    influx_user = [your_db_user]
    influx_pass_file = [your_db_pwd_txt_file]
    influx_db = "attendanceInformation"
    measurement = "Bluetooth"

    influx_client = clientRegistering(influx_host, influx_port, influx_user, influx_pass_file, influx_db)

    print('[INFO]',datetime.datetime.now())
    scheduler = BackgroundScheduler()
    scheduler.add_job(dailyAlerting, args=[influx_client, measurement, 'Band', 'C1:E3:78:ED:65:56'], trigger='interval', days=1, start_date='2020-02-14 8:30:00')
    scheduler.start()

    time.sleep(2)
    while True:
        reg_data = zip(targetDevNames,targetDevAddrs)
        targetScanning(influx_client, reg_data)