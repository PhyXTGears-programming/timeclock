from threading import Thread

from guiType import main as guiMain
from autoClockout import main as autoClockoutMain


autoclockout = Thread(target=autoClockoutMain, daemon=True)  # autoclockout
autoclockout.start()
guiMain()

autoclockout.join(0)
