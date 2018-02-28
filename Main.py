from threading import Thread

from autoClockout import main as autoClockoutMain
from guiType import main as guiMain

autoclockout = Thread(target=autoClockoutMain, daemon=True)  # autoclockout
autoclockout.start()
guiMain()

autoclockout.join(0)
