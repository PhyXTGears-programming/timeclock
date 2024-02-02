import os
import sys
from datetime import datetime, timedelta

MAX_NAME = 24

defaultOptions = {
        "ioForm": "%H:%M:%S %d.%m.%Y",
        "pathTime": "./times/",
        "autoClockOut": "00:00:00",
        "autoClockLim": "04:30:00",
        "usernameFile": "usernameFile.txt",
        "adminPass": "",
        "seasons": {
            "Build": {
                "start": "00:00:00 06.01.2018",
                "end": "23:59:59 20.02.2018",
                "hoursPerWeek": 0
            },
            "Competition": {
                "start": "00:00:00 21.03.2018",
                "end": "23:59:59 14.04.2018",
                "hoursPerWeek": 0
            }
        },
        "positions": ["Student", "Mentor", "Adult", "Other"],
        "teams": ["Programming", "Mechanical", "Media", "Woodworking", "Mentors", "Other"]
    }

def loadOpts():
    opts = {}
    try:
        import rapidjson
        print(__file__)
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        if not os.path.exists("opts.json"):
            generateDefaultOpts()
        with open("opts.json") as optsFile:  # load options
            opts = rapidjson.load(optsFile)
        return opts
    except ImportError as e:
        return defaultOptions

def loadUsers(opts):
    users = []
    for line in open(opts["usernameFile"], "r+"):
        # name | username | title | jobs
        user = line.strip().split(" | ")
        users.append(user)

    return users

def calcUserTime(opts, name, startIO=None, endIO=None):
    if len(name) > MAX_NAME:
        name = name[:MAX_NAME]
    filename = opts["pathTime"] + name.strip().replace(" ", "") + \
        ".txt"  # generate filename

    # ensure the file exists
    try:
        open(filename, "r").close()
    except FileNotFoundError:
        print(name + "'s file was not found!")
        return 0

    # should the times be between specific dates?
    checkTimes = False
    if startIO != None and endIO == None:
        raise ValueError("startIO defined, but endIO not defined")
    if startIO == None and endIO != None:
        raise ValueError("endIO defined, but startIO not defined")
    if startIO != None and endIO != None:
        checkTimes = True
        startIO = datetime.strptime(startIO, opts["ioForm"])
        endIO = datetime.strptime(endIO, opts["ioForm"])

    currentDate = datetime.now()
    lastTime = datetime.now()
    lastState = "n"
    totalTime = 0
    lineNum = 0

    for line in open(filename, "r"):
        lineNum += 1

        line = line.strip().split(" | ")
        if not line:
            continue  # if nothing on line, skip line

        if (2 > len(line)):
            print("Error reading line %d in file %s.  Found '%s'" % (lineNum, filename, line))
            continue

        state = line[0]
        linetime = line[1]
        datatime = datetime.strptime(linetime, opts["ioForm"])

        if state in "!@":
            continue  # ensure this isnt a double

        if checkTimes and datatime < startIO:
            continue  # skip until in timeframe

        if state == "i":
            pass
        elif state == "o":
            if lastState == "i":
                totalTime += (datatime - lastTime).total_seconds()

        lastTime = datatime
        lastState = state

        if checkTimes and datatime > endIO:
            break  # if left timeframe then finish

    else:  # if finished with no breaks
        # add current time if still signed in
        if lastState == "i":
            totalTime += (currentDate - lastTime).total_seconds()

    return totalTime

opts = loadOpts()
users = loadUsers(opts)

print("%24s\t%16s\t%s" % ("Name", "Position", "Hours"))

for user in users:
    name = user[0].strip()
    position = user[2]

    totalTime = calcUserTime(opts, name)
    print("%24s\t%16s\t%5.1f" % (name, position, totalTime / 3600))
