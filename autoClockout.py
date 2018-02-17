# auto clock out at midnight or whatever
from os import listdir
from time import sleep, strftime

from guiType import refreshListboxes
from ioServ import loadOpts

opts = loadOpts()


def main():
	while True:
		currenttime = strftime("%H:%M:%S")

		if currenttime == strftime("%H:00:00"):
			refreshListboxes()

		if currenttime == opts['autoClockOut']:
			for item in listdir(path=opts['pathTime']):
				io = []
				with open(opts['pathTime'] + item) as i: io = i.readlines()
				if io: io = io[-1].split(' | ')
				else: continue

				if io[0] == 'i':
					io[0] = 'a'
					with open(opts['pathTime']+item, 'a') as i: i.write(' | '.join(io))
			refreshListboxes()

			sleep(1)
		sleep(60-int(strftime('%S')))

if __name__=='__main__': main()