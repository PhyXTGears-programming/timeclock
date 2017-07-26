"""
Slack Notification Service.py

Add-on code that runs independently of PhyXTGearsTimeClock.py. Sends summary of
the past week every Sunday evening.
"""


import time
import smtplib
from settingsFile import Settings



# Sign-in and recipient credentials:
######################################################################
emailFrom="1720time@gmail.com"                      # Gmail address
password="time1720"                                 # Gmail password
emailTo="i6m9n9d4u9k2i2x2@phyxtgears1720.slack.com" # Slack bot address
######################################################################



# Send email (subject=None body=msg):
# Side note: This is the simplest method I found to email from python.
#            Other methods are available, like ones that can send with
#            a subject, but the code is much longer. I chose this for
#            simplicity, and because Slack doesn't list the subject if
#            there is none, so it doesn't look bad.
######################################################################
def sendMail(msg):
   server = smtplib.SMTP('smtp.gmail.com',587)
   server.starttls()
   server.login(emailFrom,password)
   server.sendmail(emailFrom,emailTo,msg)
######################################################################



# Return current day, hour, minute, second
# Example: "Sunday", 17, 20, 00
######################################################################
def getTime():
   day=time.strftime("%A")
   hour=int(time.strftime("%H"))
   minute=int(time.strftime("%M"))
   second=int(time.strftime("%S"))
   return day, hour, minute, second
######################################################################



# Check if a certain date is within the past week (return bool):
######################################################################
def withinOneWeek(date):
    ## date = "ddd/yyyy"
    slashIndex  = date.index("/")          # Index of slash in date
    dayToCheck  = int(date[:slashIndex])   # Day from date
    yearToCheck = int(date[slashIndex+1:]) # Year from date
    thisDay     = int(time.strftime("%j")) # Integer of day of year
    thisYear    = int(time.strftime("%Y")) # Integer of this year

    maxDays=365            # Set maxDays
    if yearToCheck%4==0:   # Accounting for leap years
        maxDays=366        # If yeap year, change maxDays to 366

    valid=False                  # Set this date to be invalid
    if yearToCheck<thisYear:     # If the week spans two years:
        thisDay+=maxDays         #  Set thisDay to thisDay + maxDays
    if (dayToCheck+7) > thisDay: # If the day is no more than 7 old
        valid=True               #  Set the day to valid
    return valid                 # Return bool
######################################################################



# Calculate the amount of hours each person put in during the last week
# Return: single text string, one person per line
# Anyone with no time is not listed
# People sorted alphabetically by first name
######################################################################
def calculatePastWeek():

    ## Import Calculations_Service and change settings temporarily:
    import Calculations_Service
    Calculations_Service.Settings['short']=True
    Calculations_Service.Settings['hours']=True
    Calculations_Service.Settings['year']=True
    Calculations_Service.Settings['minutesFile']=False

    ## Call the Calculations_Service function calculate, which processes everything:
    Calculations_Service.calculate(False) # Passing False so it doesn't print anything

    ## Collect all the people and hours within 1 week:
    timeDict={} # timeDict={name:hours}
    for name in Calculations_Service.dateDict: # dateDict={name:{date:hours}}
        for date in Calculations_Service.dateDict[name]:
            if (withinOneWeek(date) and                # Valid date
                Calculations_Service.dateDict[name][date]!="Forgot"): # Didn't forget
                if name not in timeDict: # First time:
                    timeDict[name]=Calculations_Service.dateDict[name][date]
                else:                    # All other times:
                    timeDict[name]+=Calculations_Service.dateDict[name][date]

    ## Take timeDict data, round the numbers, and put in readable form.
    ## Slightly cumbersome method, but I had to format as a dictionary          
    ## for random access, a list for sorting, and string for returning.
    alist=[] # alist=["John Pugsley: 8.35 hours\n",etc.]
    for name in timeDict:
        time=str(timeDict[name]) # Make into string from float
        time=time[:time.index(".")+3] # Round to 2 decimal places
        alist.append(name+": "+time+" hours\n")
    alist.sort() # Sort everyone alphabetically
    result=""
    for person in alist: # Convert from list to string. 1 item = 1 line
        result+=person
    return result
######################################################################

def daysFromNow(now,then):
    dayList=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    index1=dayList.index(now)
    index2=dayList.index(then)
    if index1<=index2:
        return index2-index1
    else:
        return index2+7-index1

def timeFromNow(now,thn):
	dayList=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	now = now.split()
	nowDay = dayList.index(now[0])
	tmp = now[1].split(":")
	nowHour= int(tmp[0])
	nowMin = int(tmp[1])
	nowSec = int(tmp[2])
	#print("Now: ",nowDay,nowHour,nowMin,nowSec)
	
	thn = thn.split()
	thnDay = dayList.index(thn[0])
	tmp = thn[1].split(":")
	thnHour= int(tmp[0])
	thnMin = int(tmp[1])
	thnSec = int(tmp[2])
	#print("Thn: ",thnDay,thnHour,thnMin,thnSec)
	
	difTot = (((thnDay*24+thnHour)*60+thnMin)*60+thnSec)-(((nowDay*24+nowHour)*60+nowMin)*60+nowSec)
	if difTot<0: difTot += 604800
	#print("Toht: ", difTot)
	return difTot

  

def main():
    while True:
        day,hour,minute,sec=getTime()
        time.sleep(abs(timeFromNow(str(day)+" "+str(hour)+":"+str(minute)+":"+str(sec), Settings["updateTime"])))
        data=calculatePastWeek()
        if data=="": data="No one signed in last week"
        while int(time.strftime("%S"))!=0: time.sleep(0.1)
        sent=False
        tries=0
        while not sent and tries<6:
           try:
              sendMail(data)
              sent=True
              #print("sent mail data")
           except: # No internet, or other unforseen problem
              tries+=1
              time.sleep(5) # wait for 1 minute total

if __name__=="__main__":
   main()
