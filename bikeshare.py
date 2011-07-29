import urllib2
from BeautifulSoup import BeautifulStoneSoup
import csv
from datetime import datetime, date

"""Fetch XML on Capital Bikeshare station occupancy via cronjob, say every 15 minutes, and compile into a CSV for
analysis over time."""

html = urllib2.urlopen('http://capitalbikeshare.com/stations/bikeStations.xml').read()
soup = BeautifulStoneSoup(html)

lastupdate = soup.stations['lastupdate']
headers = ['id','name','terminalname','lat','long','installed','locked','temporary','nbbikes','nbemptydocks','nbemptydocks']
stations = []

now = datetime.now()

for s in soup.stations.findAll('station'):
    row = [ now.strftime('%A'), now.year, now.month, now.day, now.hour, now.minute, lastupdate, s.id.string, s.find('name').string, \
        s.terminalname.string, s.lat.string, s.long.string, \
        s.locked.string, s.temporary.string, s.installed.string, \
        s.nbbikes.string, s.nbemptydocks.string ]
    stations.append( row )

fout = csv.writer( open('bikeshare.csv','a') )
for r in stations:
    fout.writerow(r)


"""
<stations lastUpdate="1311019547339" version="2.0">
<station>
<id>1</id>
<name>20th & Bell St</name>
<terminalName>31000</terminalName>
<lat>38.8561</lat>
<long>-77.0512</long>
<installed>true</installed>
<locked>false</locked>
<installDate/>
<removalDate/>
<temporary>false</temporary>
<nbBikes>2</nbBikes>
<nbEmptyDocks>9</nbEmptyDocks>
</station>"""
