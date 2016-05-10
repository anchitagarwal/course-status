from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

def launchMyASU(url, username, password):
	driver.get(url)
	login(username, password)

def login(username, password):
	driver.find_element_by_id('username').send_keys(username)
	driver.find_element_by_id('password').send_keys(password)
	driver.find_element_by_id('username').submit()

def classSearch(courseNumber):
	driver.get("https://webapp4.asu.edu/catalog/?t=2167")
	driver.find_element_by_id('subjectEntry').send_keys(courseNumber.split()[0])
	driver.find_element_by_id('catalogNbr').send_keys(courseNumber.split()[1])
	driver.find_element_by_name("catalogNbr").send_keys(Keys.RETURN)
	isCourseAvailable()

def isCourseAvailable():
	src = driver.page_source
	if isinstance(src, unicode):
		src = src.encode('utf-8')
	for line in src.splitlines():
		if re.match(r"\s*<img.*alt=\"seats.*>", line):
			seatsLine = line
			break
	# print seatsLine
	if re.match(r".*triangle.*", seatsLine):
		print "Bad luck man! Try again later :)"
	elif re.match(r".*circle.*", seatsLine):
		print "Seats open, gogogo!"

def quitBrowser():
	driver.quit()

MY_ASU_URL = "https://weblogin.asu.edu/cas/login?service=https%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%252Fmyasu%252F%253Finit%253Dfalse"
USERNAME = "aagarw41"
PASSWORD = "Biloran08?"
COURSE = "CSE 575"
driver = webdriver.Firefox()
launchMyASU(MY_ASU_URL, USERNAME, PASSWORD)
classSearch(COURSE)
quitBrowser()