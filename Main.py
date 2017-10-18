from threading import Thread

import autoClockout
import guiType

autoclockout = Thread(target=autoClockout.main, daemon=True)  # autoclockout
autoclockout.start()
guiType.main()

autoclockout.join(0)
