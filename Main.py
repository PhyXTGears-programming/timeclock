from importlib import reload
from threading import Thread
from time import sleep

import ioService
import autoClockout
# import 

ac = Thread(target=autoClockout.main)
ac.start()
ioService.main()

# slack service, just copy the old file
#sn = Thread(target=slackNotifService.main)
#sn.start()
