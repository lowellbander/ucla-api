import re
import urllib2
from bs4 import BeautifulSoup

class Department:    
    def __init__(self, c, n):
        self.code = c
        self.name = n

class Course:    
    def __init__(self, c, n):
        self.code = c
        self.name = n

class Listing:
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
def get_listing_data(dept,course):
    #creates a BSoup object with parse tree from url
    base = "http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel="+dept+"&idxcrs="+course
    base = base.replace(' ', '%20')            
    opener = urllib2.build_opener()
    url_opener = opener.open(base)
    page = url_opener.read()
    soup = BeautifulSoup(page) 

    #scrapes across the registrar table
    idnumber = []
    for elem in soup.find_all("span", id=re.compile("lblIDNumber")):
        idnumber.append(elem.text.strip())

    acttype = []
    for elem in soup.find_all("span", id=re.compile("lblActType")):
        acttype.append(elem.text.strip())

    days = []
    for elem in soup.find_all("span", id=re.compile("lblDays")):
        days.append(elem.text.strip())

    secnum = []
    for elem in soup.find_all("span", id=re.compile("lblSectionNumber")):
        secnum.append(elem.text.strip())

    tstart = []
    for elem in soup.find_all("span", id=re.compile("lblTimeStart")):
        tstart.append(elem.text.strip())

    tend = []
    for elem in soup.find_all("span", id=re.compile("lblTimeEnd")):
        tend.append(elem.text.strip())

    building = []
    for elem in soup.find_all("span", id=re.compile("lblBuilding")):
        building.append(elem.text.strip())

    room = []
    for elem in soup.find_all("span", id=re.compile("lblRoom")):
        room.append(elem.text.strip())

    rest = []
    for elem in soup.find_all("span", id=re.compile("Restrict")):
        rest.append(elem.text.strip())

    etotal = []
    for elem in soup.find_all("span", id=re.compile("EnrollTotal")):
        etotal.append(elem.text.strip())

    ecap = []
    for elem in soup.find_all("span", id=re.compile("EnrollCap")):
        ecap.append(elem.text.strip())

    wtotal = []
    for elem in soup.find_all("span", id=re.compile("WaitListTotal")):
        wtotal.append(elem.text.strip())

    wcap = []
    for elem in soup.find_all("span", id=re.compile("WaitListCap")):
        wcap.append(elem.text.strip())

    status = []
    for elem in soup.find_all("span", id=re.compile("Status")):
        status.append(elem.text.rstrip("\n").strip())

    listings = []
    for i in range(len(idnumber)):
        listing = Listing(idnumber[i],acttype[i],days[i],secnum[i],tstart[i],tend[i],building[i],room[i],rest[i],etotal[i],ecap[i],wtotal[i],wcap[i],status[i])
        listings.append(listing)
    return listings

#returns list of all departments
def get_depts():
    #creates a BSoup object with parse tree from url
    base = "http://www.registrar.ucla.edu/schedule/schedulehome.aspx"
    opener = urllib2.build_opener()
    url_opener = opener.open(base)
    page = url_opener.read()
    soup = BeautifulSoup(page) 
    
    #adds all department codes to array (ex: COM SCI)
    codes = []
    for elem in soup.find_all("option"):
        codes.append(elem['value'].strip())           
   
   #adds all department names to array (ex: Computer Science)
    names = []    
    for elem in soup.find_all("option"):
        names.append(elem.text.strip())

    #removes years from arrays (winter 2013, fall 2012, etc.)
    codes = codes[4:]
    names = names[4:]

    depts = []
    for i in range(len(codes)):
        d = Department(codes[i],names[i])
        depts.append(d)

    return depts

#returns list of all courses in a department
def get_courses(dept):
    #creates a BSoup object with parse tree from url
    base = "http://www.registrar.ucla.edu/schedule/crsredir.aspx?termsel=13S&subareasel="+dept
    opener = urllib2.build_opener()
    url_opener = opener.open(base)
    page = url_opener.read()
    soup = BeautifulSoup(page)

    #adds all department codes to array (ex: COM SCI)
    codes = []
    for elem in soup.find_all("option"):
        codes.append(elem['value'].strip())           
   
   #adds all department names to array (ex: Computer Science)
    names = []    
    for elem in soup.find_all("option"):
        names.append(elem.text.strip())

    #removes years from arrays (winter 2013, fall 2012, etc.)
    codes = codes[4:]
    names = names[4:]

    courses = []
    for i in range(len(codes)):
        course = Course(codes[i],names[i])
        courses.append(course)

    return courses



depts = get_depts()
dept = depts[4].code
print dept

courses = get_courses(dept)
course = courses[0].code
print courses[0].name

data = get_listing_data(dept,course)
print data[0].room
