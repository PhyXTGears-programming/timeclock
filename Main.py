from threading import Thread

import guiType
import autoClockout

autoclockout = Thread(target=autoClockout.main, daemonic=True).start() # autoclockout
guiType.main()

autoclockout.join(0)