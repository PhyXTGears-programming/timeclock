from threading import Thread

import guiType
import autoClockout

autoclockout = Thread(target=autoClockout.main, daemon=True) # autoclockout
autoclockout.start()
guiType.main()

autoclockout.join(0)