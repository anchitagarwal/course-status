# Course status in MyASU portal

This repository contains script that automates checking course status. It sends an email and an SMS to your mobile number if the seat is open for your course. Also launches it as a daemon that runs on OS X, that runs periodically with user specified time interval.
There are two files, the python script and the plist file.

### Script
***
The script takes in the following inputs:
_(Currently they need to be entered in the script itself. Can be altered to read input from a file.)_
- MyASU username/password
- Course number (e.g. CSE xxx)
- Gmail username/password (To send out email when the seat opens)
- Twilio account details (A semi-free service that lets you send SMS over the net, process explained later)
  - Twilio account SID
  - Twilio account auth token
  - Twilio number
  - Your personal number

As there are no API's to connect to MyASU server (or I'm not aware of them yet), the script uses `selenium` package to automate the task flow. Firefox is the required browser.

###### Packages installed
------
Two packages needs to be installed:
- `selenium`
- `twilio`

If you have `pip` installed, you can run the following commands:
- `pip install selenium`
- `pip install twilio`

Note: If `pip` isn't installed on your machine, do `python get-pip.py`


###### Twilio account setup
------
1. Open [Twilio](https://www.twilio.com/)
2. Sign up, log in and navigate to [Console Dashboard](https://www.twilio.com/console)
3. Note down the **Account SID** and **Auth Token**
4. Navigate to [Phone Numbers Dashboard](https://www.twilio.com/console/phone-numbers/dashboard)
5. Register for a free number (Generally has a limit for monthly SMS. But it will be enough for this script.)
6. This number will be your **Twilio Number**


### plist - Configuration property list file
***
The __configuration property list file__ contains information about your daemon. Specifying this information in a property list file lets _launchd_ register the corresponding file descriptors and launch the daemon only after a request arrives for the daemon's service.

After the property list file is created, it can be launched with the following command
`launchctl load <plist_file_path>`
This loads your property file to the LaunchDaemons folder which is used by launchd to run the daemon when a request is received.
The daemon can be stopped with the following command
`launchctl unload <plist_file_path>`
Note: `launchctl list` displays all the daemons currently active. To learn more, please visit [Daemons and Services Programming Guide](https://developer.apple.com/library/mac/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/Introduction.html)
