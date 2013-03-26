import os
from urlscrape import get_listings
from urlscrape import get_depts
from urlscrape import get_courses
from urlscrape import is_any_open
from urlscrape import is_open
from firebase import firebase
import requests,json,random

def post_urls():
	base = firebase.FirebaseApplication('https://ucla-api.firebaseio.com/urls', None)
	urls = write_urllist()
	for url in urls:
		new_url = {"value": url }
		base.post('/urls', new_url)

def get_urls():
	url = "https://ucla-api.firebaseio.com/urls.json"
	r = requests.get(url)
	c = r.content
	url_json = json.loads(c)
	urls = []
	for key in url_json:
		urls.append(url_json[key]["value"])
	return urls

def post_request(dept,course,ctype,section,name,phone,carrier,email):
	base = firebase.FirebaseApplication('https://ucla-api.firebaseio.com/requests', None)	
	request = {"dept": dept, "course" : course, "type" : ctype, "section" : section, "name" : name, "phone" : phone, "carrier" : carrier, "email" : email, "satisfied" : "0"}
	result = base.post('/requests', request)

def check_requests():
	url = "https://ucla-api.firebaseio.com/requests.json"
	r = requests.get(url)
	c = r.content
	request_json = json.loads(c)
	request = []
	for key in request_json:
		dept = request_json[key]["dept"]
		course = request_json[key]["course"]
		ctype = request_json[key]["type"]
		section = request_json[key]["section"]
		name = request_json[key]["name"]		
		email = request_json[key]["email"]	
		sat = request_json[key]["satisfied"]		
		if(sat == "0" and is_open(dept,course,ctype,section)):
			c = "'"+dept.code + ' ' + course.code +"'"
			os.system("php sendmail.php " + email + " " + c)
		
	
	

# allcourses = []
# depts = get_depts()
# for dept in depts:
# 	courses = get_courses(dept.code)
# 	print dept.code
# 	for course in courses:
# 		allcourses.append(course)

# print len(allcourses)
# randos = []
# for i in range(50):
# 	num = random.randint(0,len(allcourses)-1)
# 	randos.append(allcourses[num])

# print "start here"
# for rand in randos:
# 	status = "Closed"
# 	if(is_any_open(rand.dept,rand.code)):
# 		status = "Open"
# 	print rand.dept + " " + rand.code + ": " + status

# post_request("COM SCI", "0032","LEC", "1", "Shahid Chohan", "7145857755", "ATT", "shazeline@gmail.com")