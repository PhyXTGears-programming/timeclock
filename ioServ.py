import os
import sys
from datetime import datetime, timedelta
from math import floor
from time import strftime

import guiType

loadOptions = True
defaultOptions = fileData = {"ioForm": "%H:%M:%S %d.%m.%Y", "pathTime": "./times/", "autoClockOut": "00:00:00",
                             "autoClockLim": "04:30:00", "usernameFile": "usernameFile.txt", "adminPass": "",
                             "seasons": {"Build": {"start": "00:00:00 06.01.2018", "end": "23:59:59 20.02.2018", "hoursPerWeek": 0},
                                         "Competition": {"start": "00:00:00 21.03.2018", "end": "23:59:59 14.04.2018", "hoursPerWeek": 0}},
                             "positions": ["Student", "Mentor", "Adult", "Other"],
                             "teams": ["Programming", "Mechanical", "Media", "Woodworking", "Mentors", "Other"]}

try:
    import rapidjson
except ImportError, e:
    print("Please install the rapidjson library so the so the options file can be loaded.")
    loadOptions = False

# if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])
# open(opts["name.txt"], "a").close() # create name file if it doesnt exist


def loadOpts():
    opts = {}
    if loadOptions:
        os.chdir(os.path.dirname(__file__))
        if not os.path.exists("opts.json"):
            generateDefaultOpts()
        with open("opts.json") as optsFile:  # load options
            opts = rapidjson.load(optsFile)
        return opts
    else:
        return defaultOptions


def generateDefaultOpts():
    print("generated opts")

    # BuildHrsRqd : 54
    os.chdir(os.path.dirname(__file__))
    with open("opts.json", "w") as optsFile:
        rapidjson.dump(defaultOptions, optsFile, indent=2)


opts = loadOpts()


def signIO(n, c):
    nameIO = n
    timeIO = strftime(opts["ioForm"])
    pathIO = opts["pathTime"] + nameIO.replace(" ", "") + ".txt"

    msg, color = "Nothing", "black"

    open(pathIO, "+a").close()  # make file if it doesn"t exist
    with open(pathIO, "+r") as f:
        lines = [line.strip() for line in f]

    inTimeFrame = False
    if lines:
        lim = [int(x) for x in opts["autoClockLim"].split(":")]

        theNow = datetime.now()
        theIOA = datetime.strptime(lines[-1][5:], opts["ioForm"])
        theLIM = theIOA.replace(
            hour=lim[0], minute=lim[1], second=lim[2], microsecond=0) + timedelta(days=1)

        inTimeFrame = theIOA < theNow < theLIM

    name1st = nameIO.split()[0]  # first name
    if lines and lines[-1][0] == "a" and c == "o" and inTimeFrame:
        ## RECOVERING AUTOCLOCKOUT ##
        with open(pathIO, "w+") as f:
            f.write("\n".join(lines[:-1]) + "\n" + c + " | " + timeIO + "\n")
        msg, color = name1st + " signed out proper!", "green"
        return msg, color
    elif lines and lines[-1][0] == "a" and c == "i" and inTimeFrame:
        ## SIGNING IN WHEN SEMI CLOCKED OUT ##
        msg, color = "Did you mean to sign out to recover hours, " + name1st + "?", "orange"

    elif lines and ((lines[-1][0] in "i!" and c == "i") or (lines[-1][0] in "o@" and c == "o") or (lines[-1][0] == "a" and c == "o" and not inTimeFrame)):
        ## DOUBLE SIGN IN/OUT ##
        color = "orange"
        if c == "i":
            msg = name1st + " is already signed in!"
            c = "!"
        elif c == "o":
            if lines[-1][0] in "o@":
                msg = name1st + " is already signed out!"
            elif lines[-1][0] == "a":
                msg = name1st + " was auto-signed out!"
            c = "@"
        # return msg,color

    elif not lines and c == "o":
        ## NEVER SIGNED IN BEFORE ##
        msg, color = name1st + " has never signed in!", "orange"
        return msg, color
    else:
        ## NORMAL SIGN IN ##
        hrs = 0
        inSeason = False
        currentSeason = "Off"
        timet = 0
        for season in opts["seasons"]:
            v = calcSeasonTime(nameIO, season)
            inSeason, timet = v[0], v[1]
            timet = min(int(timet // 3600), 999)
            currentSeason = season
            if inSeason:
                break
        else:
            currentSeason = "Off"
            timet = min(int(calcTotalTime(nameIO) // 3600), 999)

        limit = "8"
        if currentSeason + "Hrs/Wk" in opts:
            limit = str(opts[currentSeason + "Hrs/Wk"])

        # calculate total time in seconds then convert to hours (rounded 2 dec places)
        hours = str(floor(hrs / 3600 * 100) / 100)
        weekh = str(floor(calcWeekTime(nameIO.replace(" ", "")) /
                          3600 * 100) / 100)  # calculate current week time
        if c == "i":
            msg, color = name1st + " signed in! " + hours + \
                " hours.\n" + weekh + " of " + limit + " hours.", "Green"
        elif c == "o":
            msg, color = name1st + " signed out! " + hours + \
                " hours.\n" + weekh + " of " + limit + " hours.", "Red"

    with open(pathIO, "a+") as f:
        f.write(c + " | " + timeIO + "\n")

    return msg, color


def checkNameDB(n):  # check for if a name exists already
    for line in open(opts["usernameFile"]):
        for item in line.split("|"):
            if item.lower().replace(" ", "") == n.lower().replace(" ", ""):
                return True
    return False


def addNameDB(full, user, title="None", job="None"):  # add a new name to the list
    file = open(opts["usernameFile"], "a+")
    file.write(" | ".join([full.title(), user.lower(), title, job]) + "\n")
    file.close()


def sortUsernameList():  # alphebetize names
    def findCapitals(s):  # for generating usernames
        letters = ""
        for i in s:
            if i.isupper():
                letters += i
        return letters

    with open(opts["usernameFile"]) as u:
        names = []
        for l in u.readlines():
            l = l.strip().split(" | ")
            l[0] = l[0].title()  # full name
            if len(l) >= 2:  # user key
                l[1] = l[1].lower()
            else:
                l += [findCapitals(l[0]).lower()]
            if len(l) < 3 or l[2] == "":
                l += ["none"]  # if no title listed
            if len(l) < 4 or l[3] == "":
                l += ["none"]  # if no job listed

            names += [" | ".join(l[:4]) + "\n"]
        names.sort()
    with open(opts["usernameFile"], "w") as f:
        f.write("".join(names))


def calcTotalTime(n):
    return calcUserTime(n)


def calcWeekTime(n):
    dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    firstDayOfWeek = (dt - timedelta(days=dt.isoweekday()))  # last sunday
    lastDayOfWeek = (firstDayOfWeek + timedelta(days=7))  # next sunday

    firstDayOfWeek = firstDayOfWeek.strftime(opts["ioForm"])
    lastDayOfWeek = lastDayOfWeek.strftime(opts["ioForm"])

    return calcUserTime(n, startIO=firstDayOfWeek, endIO=lastDayOfWeek)


def calcSeasonTime(name, season, ignoreCheck=False):
    if not ignoreCheck and not (datetime.strptime(opts["seasons"][season]["start"], opts["ioForm"]) <= datetime.now() <= datetime.strptime(opts["seasons"][season]["end"], opts["ioForm"])):
        return False, 0, 0

    currentDate = datetime.now()
    buildStart = datetime.strptime(
        opts["seasons"][season]["start"], opts["ioForm"])
    buildLeave = datetime.strptime(
        opts["seasons"][season]["end"], opts["ioForm"])

    buildDelta = currentDate - buildStart

    daysSinceStart = max(buildDelta.days, 0)

    totalTime = calcUserTime(
        name, startIO=opts["seasons"][season]["start"], endIO=opts["seasons"][season]["end"])

    return True, totalTime, daysSinceStart


def calcUserTime(name, startIO=None, endIO=None):
    if len(name) > guiType.maxName:
        name = name[:guiType.maxName]
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

    for line in open(filename, "r"):
        line = line.strip().split(" | ")
        if not line:
            continue  # if nothing on line, skip line

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


def calcUserData(name):
    userdata = name + "'s TimeData\n"
    userdata += "Total Time: " + str(calcUserTime(name) // 3600)
    for season in opts["seasons"]:
        try:
            if opts["seasons"][season]["start"] and opts["seasons"][season]["end"]:
                userdata += "\n" + season + " Time: " + \
                    str(calcSeasonTime(name, season,
                                       ignoreCheck=True)[1] // 3600)
        except KeyError:
            print("Season \"" + season + "\" does not exist in opts.txt! Please give it a " +
                  season + "Start and " + season + "Leave time value!")

    return userdata


def mkfile(t): open(t, "a+").close()  # make files if they dont exist


def loadUsers():
    allusers = {}
    for line in open(opts["usernameFile"], "r+"):
        l = line.split(" | ")  # name | username | title | jobs
        allusers[l[2]] = (allusers[l[2]] or []) + []


def calcSlackTimeString():
    names = []
    seasontimes = {}

    longestname = 0
    currentSeason = "Off"

    for line in open(opts["usernameFile"], "r+"):
        name = line.strip().split(" | ")[0]
        print(name)
        names += [name]
        longestname = max(len(name), longestname)

        inSeason = False
        timet = 0
        days = 0
        for season in opts["seasons"]:
            inSeason, seasontimes[name], days = calcSeasonTime(name, season)
            currentSeason = season
            if inSeason:
                break
        else:
            currentSeason = "Off"
            seasontimes[name], days = calcWeekTime(name), 0

        seasontimes[name] = int(seasontimes[name] // 3600)

    topstr = "Name" + " " * (longestname - 4) + \
        " - Season (" + currentSeason + ")\n\n"

    for name in names:
        totaltime = str(times[name])
        seasontime = str(seasontimes[name])
        topstr += name + " " * (longestname - len(name)) + " - " + \
            " " * (5 - len(seasontime)) + str(seasontimes[name]) + "\n"

    return "```" + topstr + "```"
