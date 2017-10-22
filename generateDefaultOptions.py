import os

fileString = """
ioForm : %H:%M:%S %d.%m.%Y # Leave this unless you know what you are doing, this sets the format the time is written to the text files
pathTime : ./times/ # path to store times
autoClockOut : 00:00:00 # time to automatically sign out everyone signed in (00:00:00 is midnight)
autoClockLim : 05:00:00 # If the person signs out before this time, the auto clock out is not counted
usernameFile : usernameFile.txt # file to save usernames in
adminPass : 1234 # passcode used to shut down program when it is full screen
hoursLocation : enterLoationOf_timeclock-hours # location of PhyXTGears-programming/timeclock library
# If you leave hoursLocation the same, most time calculation functions will be disabled
# hoursLocation should be the path to the main folder of the library with a slash after it (eg. "../../timeclock-hours/")
"""

os.chdir(os.path.dirname(__file__))
input("Press enter to overwrite current options file with the default")
with open('opts.txt', 'w') as fil:
    fil.write(fileString.strip())
