import re
import urllib2
from bs4 import BeautifulSoup

url = "http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel=CHEM&idxcrs=0014C+++"
opener = urllib2.build_opener()
url_opener = opener.open(url)
page = url_opener.read()
soup = BeautifulSoup(page) 

acttype = []
for elem in soup.find_all("span", id=re.compile("lblActType")):
    acttype.append(elem.text)

secnum = []
for elem in soup.find_all("span", id=re.compile("lblSectionNumber")):
    secnum.append(elem.text)

tstart = []
for elem in soup.find_all("span", id=re.compile("lblTimeStart")):
    tstart.append(elem.text)

tend = []
for elem in soup.find_all("span", id=re.compile("lblTimeEnd")):
    tend.append(elem.text)

building = []
for elem in soup.find_all("span", id=re.compile("lblBuilding")):
    building.append(elem.text)

room = []
for elem in soup.find_all("span", id=re.compile("lblRoom")):
    room.append(elem.text)

rest = []
for elem in soup.find_all("span", id=re.compile("Restrict")):
    rest.append(elem.text)

etotal = []
for elem in soup.find_all("span", id=re.compile("EnrollTotal")):
    etotal.append(elem.text)

ecap = []
for elem in soup.find_all("span", id=re.compile("EnrollCap")):
    ecap.append(elem.text)

wtotal = []
for elem in soup.find_all("span", id=re.compile("WaitListTotal")):
    wtotal.append(elem.text)

wcap = []
for elem in soup.find_all("span", id=re.compile("WaitListCap")):
    wcap.append(elem.text)

status = []
for elem in soup.find_all("span", id=re.compile("Status")):
    status.append(elem.text.rstrip("\n"))

table = []
table.append(acttype)
table.append(secnum)
table.append(tstart)
table.append(tend)
table.append(building)
table.append(room)
table.append(rest)
table.append(etotal)
table.append(ecap)
table.append(wtotal)
table.append(wcap)
table.append(status)

for j in range(len(table[0])):
    for i in range(len(table)):
        print table[i][j]
    print "\n"
