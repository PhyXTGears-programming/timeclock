from importlib import reload
from threading import Thread
from time import sleep

tc = Thread(target=timeClockService.main)
tc.start()

# slack service, just copy the old file
#sn = Thread(target=slackNotifService.main)
#sn.start()

# reload the options file
#sleep(60)
#reload(opts)