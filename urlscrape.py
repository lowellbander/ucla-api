import re
import urllib2
from bs4 import BeautifulSoup

class Department:
    def __init__(self, c, n):
        self.code = c
        self.name = n

class Course:
    def __init__(self, c, n, u):
        self.code = c
        self.name = n
        self.url = u

class Listing:
    def __init__(self, idnum, ctype, sec, days, start, stop, build, room, rest, en, encap, wait, waitcap, status,u):
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
        self.url = u

#pulls data from a class url
#for example: http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel=PHYSICS&idxcrs=0004AL++
def get_listings(dept,course):
    #creates a BSoup object with parse tree from url
    base = "http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=13S&subareasel="+dept+"&idxcrs="+course
    base = base.replace(' ', '%20')
    opener = urllib2.build_opener()
    url_opener = opener.open(base)
    page = url_opener.read()
    soup = BeautifulSoup(page)

    tags = ["lblIDNumber","lblActType","lblSectionNumber","lblDays","lblTimeStart","lblTimeEnd","lblBuilding","lblRoom","Restrict","EnrollTotal","EnrollCap","WaitListTotal","WaitListCap","Status"]
    table = []    
    for i in range(len(tags)):
        tag = tags[i]
        subtable = []
        for elem in soup.find_all("span", id=re.compile(tag)):
            subtable.append(elem.text.strip()) 
        table.append(subtable)
    # for i in range(len(table)):
    #     print table[i]
    #     print "\n"    

    listings = []    
    for i in range(len(table[0])):
        listing = Listing(table[0][i],table[1][i],table[2][i],table[3][i],table[4][i],table[5][i],table[6][i],table[7][i],table[8][i],table[9][i],table[10][i],table[11][i],table[12][i],table[13][i],base)
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
    base = base.replace(' ', '%20')       
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
        course = Course(codes[i],names[i],base)
        courses.append(course)

    return courses

def test_listing():
    test = get_listings("COM SCI", "0031")     
    for i in range(len(test)):
        print test[i].id
        print test[i].type
        print test[i].section
        print test[i].days
        print test[i].starttime
        print test[i].stoptime
        print test[i].building
        print test[i].room
        print test[i].restricted
        print test[i].enrollmenttotal
        print test[i].enrollmentcapacity
        print test[i].waitlisttotal
        print test[i].waitlistcapacity
        print test[i].status
        print test[i].url
        print "\n"

def test_all():
    depts = get_depts()
    for dept in depts:
        courses = get_courses(dept.code)
        for course in courses:
            listings = get_listings(dept.code,course.code)
            print course.name
            for listing in listings:
                print listing.type + " " + listing.section + " " + listing.status

test_listing()