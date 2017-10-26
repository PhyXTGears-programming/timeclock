from threading import Thread

import autoClockout
import guiType
#from touchtone import *

#playTone('0123456789ABCD#*')

autoclockout = Thread(target=autoClockout.main, daemon=True)  # autoclockout
autoclockout.start()
guiType.main()

autoclockout.join(0)
