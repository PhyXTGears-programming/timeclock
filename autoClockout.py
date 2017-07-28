# auto clock out at midnight or whatever
import os
import time
from optsFile import opts

def clockOutCheck():
	if time.strftime("%H:%M:%S")==opts['autoClockOut']:
		for item in os.listdir(path=opts['path']):
			io = []
			with open(opts['path']+item) as i: io = i.readlines()[-1].split()
			if io[0] == 'I':
				io[0] = 'O'
				with open(opts['path']+item, 'a') as i: i.write(' '.join(io)+'\n')
		time.sleep(1)

if __name__=='__main__': clockOutCheck()