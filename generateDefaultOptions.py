import os

os.chdir(os.path.dirname(__file__))
with open('opts.txt', 'w') as fil:
    input("Press enter to overwrite current options file with the default")
    fil.write('ioForm : %H:%M:%S %d.%m.%Y\n')
    fil.write('pathTime: ./times/\n')
    fil.write('autoClockOut: 00:00:00\n')
    fil.write('autoClockLim: 05:00:00\n')
    fil.write('usernameFile: usernameFile.txt\n')
    fil.write('adminPass: 1234\n')
    fil.write('hoursLocation: enterLoationOf_timeclock-hours\n')
