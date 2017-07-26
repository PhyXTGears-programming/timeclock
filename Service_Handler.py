from importlib import reload
from threading import Thread
from time import sleep

import settingsFile
import Slack_Notification_Service
import Time_Clock_Service


def main():
    # targets=[Slack_Notification_Service,Time_Clock_Service]
    # for t in targets:
    # t=Thread(target=t.main)
    # t.start()
    tc = Thread(target=Time_Clock_Service.main)
    tc.start()
    sn = Thread(target=Slack_Notification_Service.main)
    sn.start()

    newUpdate = False
    while not newUpdate:
        sleep(60)
        reload(settingsFile)
        newUpdate = settingsFile.Settings['newUpdate']


if __name__ == "__main__": main()