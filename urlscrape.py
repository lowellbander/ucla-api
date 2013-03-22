import re
import urllib2
from bs4 import BeautifulSoup

class Department:    
    def __init__(self, c, n):
        self.code = c
        self.name = n

class Course:
    def __init__(self, idnum, ctype, sec, days, start, stop, build, room, rest, en, encap, wait, waitcap, status):
        self.id = idnum
        self.type = ctype
        self.section = sec
        self.days = days
        self.starttime = start
        self.stoptime = stop
        self.building = build
        self.room = room
        self.restricted = rest
        self.enrollmenttotal = en
        self.enrollmentcapacity = encap
        self.waitlisttotal = wait
        self.waitlistcapacity = waitcap
        self.status = status


#pulls data from a class url
#for example: http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel=PHYSICS&idxcrs=0004AL++
def scrape_url(url):
    #creates a BSoup object with parse tree from url
    opener = urllib2.build_opener()
    url_opener = opener.open(url)
    page = url_opener.read()
    soup = BeautifulSoup(page) 

    #scrapes across the registrar table
    idnumber = []
    for elem in soup.find_all("span", id=re.compile("lblIDNumber")):
        idnumber.append(elem.text)
    
    acttype = []
    for elem in soup.find_all("span", id=re.compile("lblActType")):
        acttype.append(elem.text)

    days = []
    for elem in soup.find_all("span", id=re.compile("lblDays")):
        days.append(elem.text)

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
    
    courses = []
    for i in range(len(idnumber)):
        course = Course(idnumber[i],acttype[i],days[i],secnum[i],tstart[i],tend[i],building[i],room[i],rest[i],etotal[i],ecap[i],wtotal[i],wcap[i],status[i])
        courses.append(course)

    return courses

#returns list of all departments
def scrape_depts():
    #creates a BSoup object with parse tree from url
    base = "http://www.registrar.ucla.edu/schedule/schedulehome.aspx"
    opener = urllib2.build_opener()
    url_opener = opener.open(base)
    page = url_opener.read()
    soup = BeautifulSoup(page) 
    
    #adds all department codes to array (ex: COM SCI)
    codes = []
    for elem in soup.find_all("option"):
        codes.append(elem['value'])           
   
   #adds all department names to array (ex: Computer Science)
    names = []    
    for elem in soup.find_all("option"):
        names.append(elem.text)

    #removes years from arrays (winter 2013, fall 2012, etc.)
    codes = codes[4:]
    names = names[4:]

    depts = []
    for i in range(len(codes)):
        d = Department(codes[i],names[i])
        depts.append(d)

    return depts

scrape_depts()
# scrape_url("http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel=COM+SCI&idxcrs=0031++++")