# auto clock out at midnight or whatever
from os import environ, listdir
from time import sleep, strftime

from ioServ import calcSlackTimeString, loadOpts

from datetime import date, datetime, time, timedelta
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/tmp/autoclock.log')


try:
    from slacker import Slacker
    slackapiExists = True
except ImportError:
    slackapiExists = False

slacktokExists = "SLACKAPITOKEN" in environ
if slackapiExists and slacktokExists:
    slackapi = Slacker(environ["SLACKAPITOKEN"])
else:
    if not slackapiExists:
        print("Can't find \"Slacker\" SlackAPI Python module")
    elif not slacktokExists:
        print("Slack API token not found, please define it in your environment as $SLACKAPITOKEN")


opts = loadOpts()

# Given string of a particular time with format HH:MM::SS, return the equivalet time object.
def to_time(str):
    res = [ int(i) for i in str.split(":") ]
    return time(res[0], res[1], res[2])

def autoClockOut():
    pathTime = opts["pathTime"]

    logging.info("Begin auto clockout...")

    for item in listdir(path=pathTime):
        fileTime = pathTime + item
        logging.info("Check file %s" % fileTime)
        io = []
        with open(fileTime) as i:
            # Read lines from file.
            io = i.readlines()

        if io:
            # Split last line into fields.
            io = io[-1].split(" | ")
        else:
            # Go to next file.
            continue

        if io[0] in "i!":

            logging.info("Found user who failed to log out.  Auto clock out user. %s" % item)

            # Last line has an clock-in (i) or double clock-in (!) and
            # it's past time to clock out.

            # Append auto clock-out at same time as clock-in.
            io[0] = "a"
            with open(fileTime, "a") as i:
                i.write(" | ".join(io))

    logging.info("End auto clockout")

def main():
    midnight = time(0, 0, 0)
    clockoutTime = to_time(opts["autoClockOut"])
    DAY_ONE = timedelta(days=1)

    now = datetime.now()
    deadline = datetime.combine(now.date(), clockoutTime)

    if deadline < now:
        deadline = deadline + DAY_ONE

    logging.info("Next auto clockout deadline: %s" % deadline)

    while True:
        if strftime("%w") == "0" and now.time() == midnight and slackapiExists:
            print("sending to slack!")
            timeString = calcSlackTimeString()
            slackapi.chat.post_message(
                "#prog_timeclock", timeString, as_user=True)

        if now > deadline:
            deadline = deadline + DAY_ONE

            autoClockOut()

            logging.info("Next auto clockout deadline: %s" % deadline)

        sleepTime = 300 - int(strftime("%S"))

        logging.info("Sleeping for %d seconds" % sleepTime)

        sleep(sleepTime)

        now = datetime.now()

    logging.warn("Auto clockout terminated")

if __name__ == "__main__":
    main()
