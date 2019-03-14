import time
import pandas as pd
from bluetooth import *
#####################################################################
############# For Bluetooth Low Energy Device(like band) ############
# from bluetooth.ble import DiscoveryService
#####################################################################
from datetime import datetime, timedelta


myPhone = "90:C7:D8:0B:E8:E7"
# myBand = "C1:E3:78:ED:65:56"
activeDevs = []
a=[]
b=[]
tempFlag = 0
# Avoid repeated punches due to a short-lived abnormality of the Raspberry Pi or this program(such as a short power off)
df = pd.read_csv('~/RaspberryPi-Bluetooth-Punch-System/punch-in_and_punch-out_data.csv')
last_punchFlag = df.iat[-1,0]
last_punchTime = df.iat[-1,1]
last_punchDatetime = datetime.strptime(last_punchTime, '%Y-%m-%d %H:%M:%S')


while True:
	############# For Bluetooth Device(like phone) ######################
	foundDevs = discover_devices(lookup_names=True)
	for(addr,name) in foundDevs:
	#####################################################################
	############# For Bluetooth Low Energy Device(like band) ############
	# foundDevs = DiscoveryService().discover(2)
	# for(addr,name) in foundDevs.items():
	#####################################################################
			# print("[+] Found Bluetooth Device :  " +str(addr))
			activeDevs.append(addr)

	if myPhone in activeDevs and last_punchFlag == 0 and tempFlag == 0:
		a.append(time.strftime("%a", time.localtime()))
		a.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		dataframe = pd.DataFrame({'week':a[0], 'time':a[1], 'punchFlag':last_punchFlag}, index=[0])
		dataframe.to_csv("punch-in_and_punch-out_data.csv", mode='a', sep=',', index=False, header=False)
		last_punchFlag = 1
		print("Punch in : " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
		dataframe = pd.DataFrame({'week':a[0], 'time':a[1], 'punchFlag':last_punchFlag}, index=[0])
		dataframe.to_csv("punch-in_and_punch-out_data.csv", mode='a', sep=',', index=False, header=False)
		a = []
		last_punchDatetime = datetime.now()

	# Once you leave, it will not be seen as punch out immediately (You can have a break up to 10 minutes).
	if myPhone not in activeDevs and last_punchFlag == 1 and tempFlag == 0:
		tempFlag = 1
		last_punchDatetime = datetime.now()
		b.append(time.strftime("%a", time.localtime()))
		b.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		
	now_time = datetime.now()
	# If you leave more than 10 minutes, the punch out will be recorded with the time you leave 10 minutes ago (This is due to the consideration to correctly record when did you punch out).
	if myPhone not in activeDevs and tempFlag == 1 and (now_time - last_punchDatetime > timedelta(minutes=10)):
		dataframe = pd.DataFrame({'week':b[0], 'time':b[1], 'punchFlag':last_punchFlag}, index=[0])
		dataframe.to_csv("punch-in_and_punch-out_data.csv", mode='a', sep=',', index=False, header=False)
		last_punchFlag = 0
		print("Punch out : " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
		dataframe = pd.DataFrame({'week':b[0], 'time':b[1], 'punchFlag':last_punchFlag}, index=[0])
		dataframe.to_csv("punch-in_and_punch-out_data.csv", mode='a', sep=',', index=False, header=False)
		tempFlag = 0
		last_punchDatetime = datetime.now()
		b = []
	# but if you return in 10 minutes, from the view of this program, nothing happens.
	elif myPhone in activeDevs and tempFlag == 1:
		tempFlag = 0
		df = pd.read_csv('~/RaspberryPi-Bluetooth-Punch-System/punch-in_and_punch-out_data.csv')
		last_punchTime = df.iat[-1,1]
		last_punchDatetime = datetime.strptime(last_punchTime, '%Y-%m-%d %H:%M:%S')
		b = []

	activeDevs = []
	# time.sleep(10)
