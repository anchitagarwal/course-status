from selenium.webdriver.common.keys import Keys
from twilio.rest import TwilioRestClient
from selenium import webdriver
from datetime import datetime
import smtplib
import re
import os

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
	# Get current time
	now = datetime.now()
	current_time = "%s %s, %s\t%s:%s" % (now.strftime("%B"), now.day, now.year, now.hour, now.minute)
	# open log file
	logs = open('/tmp/myasu.logs', 'a+')
	# print seatsLine
	if re.match(r".*triangle.*", seatsLine):
		logs.write("[  %s  ]\tCourse %s - Bad luck man! Try again later :)\n" % (current_time, COURSE))
		logs.close()
	elif re.match(r".*circle.*", seatsLine):
		logs.write("[  %s  ]\tCourse %s - DUDE! Seats open, gogogo!\n" % (current_time, COURSE))
		sendMail()
		sendSMS()
		logs.close()

def quitBrowser():
	driver.quit()

def sendMail():
	# Connecting to SMTP server
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
	smtpObj.starttls()
	# Login
	smtpObj.login(GMAIL_USERNAME, GMAIL_PASSWORD)
	# Prepare email body
	FROM = 'seats.open@myasu.com'
	TO = 'anchit008@gmail.com'
	MESSAGE = 'From: %s\nTo: %s\nSubject: DUDE! Seats open for %s\n\nThank me later!' % (FROM, TO, COURSE)
	# Send email
	smtpObj.sendmail(FROM, TO, MESSAGE)
	smtpObj.quit()

def sendSMS():
	accountSID = "TWILIO_ACCOUNT_SID"
	authToken = "TWILIO_AUTH_TOKEN"
	twilioClient = TwilioRestClient(accountSID, authToken)
	myTwilioNumber = "TWILIO_NUMBER"
	myCellNumber = "YOUR_NUMBER"
	smsBody = "DUDE! Seats open for %s!!" % COURSE
	message = twilioClient.messages.create(body=smsBody, from_=myTwilioNumber, to=myCellNumber)

MY_ASU_URL = "https://weblogin.asu.edu/cas/login?service=https%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%252Fmyasu%252F%253Finit%253Dfalse"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
COURSE = "COURSE"
GMAIL_USERNAME = 'GMAIL_USERNAME'
GMAIL_PASSWORD = 'GMAIL_PASSWORD'
driver = webdriver.Firefox()
# switch back to previous window
switch_back_cmd = """
osascript -e 'tell application "System Events" to key code 48 using {command down}' 
"""
os.system(switch_back_cmd)
launchMyASU(MY_ASU_URL, USERNAME, PASSWORD)
classSearch(COURSE)
quitBrowser()
