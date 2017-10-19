# auto clock out at midnight or whatever
import os
import time

from guiType import refreshListboxes
from ioServ import loadOpts

opts = loadOpts()


def main():
	while True:
		if time.strftime("%H:%M:%S") == opts['autoClockOut']:
			for item in os.listdir(path=opts['pathTime']):
				io = []
				with open(opts['pathTime'] + item) as i:
					io = i.readlines()[-1].split()
				if io[0] == 'i':
					io[0] = 'a'
					with open(opts['pathTime'] + item, 'a') as i:
						i.write(' '.join(io) + ' ' + time.strftime(opts['ioform']) + '\n')
			refreshListboxes()
			time.sleep(1)
