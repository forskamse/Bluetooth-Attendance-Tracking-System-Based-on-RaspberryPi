import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# decide the month
today=datetime.date.today() 
oneday=datetime.timedelta(days=1) 
yesterday=today-oneday
month = ("%s-%s" % (yesterday.year,yesterday.month))

df = pd.read_csv('/home/pi/projects/punch-in_and_punch-out_data.csv')
# turn to datetime format
df['time'] = pd.to_datetime(df['time'])
# set datetime as index
df = df.set_index('time')

# plot
plt.plot(df[month]['punchFlag'])
plt.ylabel(u'punchFlag')
plt.xlabel(u'Time')

#Auto rotate date
plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches(30,10)
#Horizontal axis main scale
alldays =  mdates.DayLocator()
plt.gca().xaxis.set_major_locator(alldays)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
#Horizontal axis subscale
hoursLoc = mdates.HourLocator(interval=4)
plt.gca().xaxis.set_minor_locator(hoursLoc)
plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
# Set the distance between the horizontal axis and the date scale farther
plt.gca().tick_params(pad=10)
plt.grid(True)
plt.savefig("working-hours.png")
#plt.show()

