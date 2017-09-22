from threading import Thread

#import ioService
import guiType
import autoClockout

Thread(target=autoClockout.main).start() # autoclockout
guiType.main()
#ioService.main()
