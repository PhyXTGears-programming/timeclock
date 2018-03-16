# auto clock out at midnight or whatever
from os import listdir, environ
from time import sleep, strftime

from guiType import refreshListboxes
from ioServ import loadOpts, calcSlackTimeString

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


def main():
    while True:
        currenttime = strftime("%H:%M:%S")

        if currenttime == strftime("%H:00:00"):
            refreshListboxes()

        if strftime("%w") == "0" and currenttime == "00:00:00" and slackapiExists:
            print("sending to slack!")
            timeString = calcSlackTimeString()
            slackapi.chat.post_message("#programming_timeclock", timeString, as_user=True)

        if currenttime == opts["autoClockOut"]:
            for item in listdir(path=opts["pathTime"]):
                io = []
                with open(opts["pathTime"] + item) as i:
                    io = i.readlines()
                if io:
                    io = io[-1].split(" | ")
                else:
                    continue

                if io[0] in "i!":
                    io[0] = "a"
                    with open(opts["pathTime"] + item, "a") as i:
                        i.write(" | ".join(io))
            refreshListboxes()

            sleep(1)
        sleep(60 - int(strftime("%S")))


if __name__ == "__main__":
    main()
