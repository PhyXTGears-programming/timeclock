import importlib
import os
import re
import csv
from datetime import datetime

# if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])
# open(opts['name.txt'], 'a').close() # create name file if it doesnt exist


def loadOpts():
	opts = {}
	os.chdir(os.path.dirname(__file__))
	if not os.path.exists('opts.txt'):
		generateDefaultOpts()
	for line in open('opts.txt'):  # load options
		line = line.split("#")[0].strip().strip(" ")
		if line and line[0] != "#":
			line = line.strip().split(' : ')
			opts[line[0]] = line[1].split('#')[0].strip(' ')
	return opts


def generateDefaultOpts():
	print('generated opts')
	fileString = """
	ioForm : %H:%M:%S %d.%m.%Y # Leave this unless you know what you are doing, this sets the format the time is written to the text files
	pathTime : ./times/ # path to store times
	autoClockOut : 00:00:00 # time to automatically sign out everyone signed in (00:00:00 is midnight)
	autoClockLim : 05:00:00 # If the person signs out before this time, the auto clock out is not counted
	usernameFile : usernameFile.txt # file to save usernames in
	adminPass : 1234 # passcode used to shut down program when it is full screen
	"""
	os.chdir(os.path.dirname(__file__))
	# input("Press enter to overwrite current options file with the default")
	with open('opts.txt', 'w') as file:
		file.write(fileString.strip().replace("\t", ""))


opts = loadOpts()


def checkNameDB(n):  # check for if a name exists already
	for line in open(opts['usernameFile']):
		for item in line.split("|"):
			if item.lower().replace(' ', '') == n.lower().replace(' ', ''):
				return True
	return False


def addNameDB(full, user, job='none'):  # add a new name to the list
	file = open(opts['usernameFile'], 'a+')
	file.write(full.title() + '|' + user.lower() + '|' + job + '\n')
	file.close()


def findCapitals(s):
	letters = ''
	for i in s:
		if i.isupper(): letters += i
	return letters

def sortUsernameList():  # alphebetize names
	with open(opts['usernameFile']) as u:
		names = []
		for l in u.readlines():
			l = l.strip().split('|')
			l[0] = l[0].title() # full name
			if len(l)>=2: # user key
				l[1] = l[1].lower()
			else:
				l += [findCapitals(l[0]).lower()]
			if not len(l)>=3: l += ['Student'] # if no job listed

			names += ['|'.join(l)+'\n']
		names.sort()
	with open(opts['usernameFile'], 'w') as f:
		f.write(''.join(names))


def calcTotalTime(n):
	n = n.replace(' ', '')
	with open(opts['pathTime'] + n + '.txt', 'r') as userFile:
		totalTime = 0
		lastState = "n"
		lastTime = datetime.now()
		for currentLine in userFile:
			currentLine = currentLine.strip()
			if currentLine:
				time_str = currentLine[4:]
				state = currentLine[0]
				time = datetime.strptime(time_str, opts['ioForm'])
				if state == "i":
					lastTime = time
				elif state == "o":
					if lastState == "i":
						totalTime += (time - lastTime).total_seconds()
			else:
				state = "n"
			lastState = state
			lastTime = time
		return totalTime


def mkfile(t):
	open(t, 'a+').close()  # make files if they dont exist
