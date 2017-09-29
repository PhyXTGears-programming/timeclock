# auto clock out at midnight or whatever
import os
import time

opts = {}
for line in open('opts.txt'): # load options
	line = line.strip().split(' : ')
	opts[line[0]] = line[1]

def main():
	while True:
		if time.strftime("%H:%M:%S")==opts['autoClockOut']:
			print('doin it')
			for item in os.listdir(path=opts['pathTime']):
				io = []
				with open(opts['pathTime']+item) as i: io = i.readlines()[-1].split()
				if io[0] == 'i':
					io[0] = 'o'
					with open(opts['pathTime']+item, 'a') as i: i.write(' '.join(io)+' a\n')
			print('done')
			time.sleep(1)