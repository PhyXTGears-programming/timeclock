import os, re, csv, importlib
from datetime import datetime,timedelta

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
	ioForm : %H:%M:%S %d.%m.%Y
	pathTime : ./times/
	autoClockOut : 00:00:00
	autoClockLim : 05:00:00
	usernameFile : usernameFile.txt
	adminPass : 1234
	buildStart : 10:30:00 06.01.2018
	buildLeave : 23:59:59 20.02.2018
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


def sortUsernameList():  # alphebetize names
	def findCapitals(s): # for generating usernames
		letters = ''
		for i in s:
			if i.isupper(): letters += i
		return letters

	with open(opts['usernameFile']) as u:
		names = []
		for l in u.readlines():
			l = l.strip().split(' | ')
			l[0] = l[0].title() # full name
			if len(l)>=2: # user key
				l[1] = l[1].lower()
			else:
				l += [findCapitals(l[0]).lower()]
			if not len(l)>=3: l += ['Student'] # if no job listed

			names += [' | '.join(l)+'\n']
		names.sort()
	with open(opts['usernameFile'], 'w') as f:
		f.write(''.join(names))


def calcTotalTime(n):
	n = n.replace(' ', '')
	try:
		userFile = open(opts['pathTime'] + n + '.txt', 'r')
		linesFromFile = userFile.readlines()

		dt = datetime.now()
		firstDayOfWeek = dt - timedelta(days=dt.weekday()) - timedelta(days=1)
		addCurrentTime = linesFromFile and linesFromFile[-1][0]=='i' and datetime.strptime(linesFromFile[-1][4:].strip(), opts['ioForm']) > firstDayOfWeek

		totalTime = 0
		lastState = "n"
		lastTime = 0

		for currentLine in linesFromFile:
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
		if lastState == 'i' and addCurrentTime: totalTime += (datetime.now() - lastTime).total_seconds()

		userFile.close()
		return totalTime
	except FileNotFoundError:
		#print('User '+n+"'s time file not found.")
		return 0

def calcWeekTime(n):
	n = n.replace(' ','')
	try:
		userFile = open(opts['pathTime'] + n + '.txt', 'r')
		totalTime,lastTime,lastState = 0,0,'n'
		linesFromFile = userFile.readlines()

		dt = datetime.now()
		firstDayOfWeek = dt - timedelta(days=dt.weekday()) - timedelta(days=1)
		addCurrentTime = linesFromFile and linesFromFile[-1][0]=='i' and datetime.strptime(linesFromFile[-1][4:].strip(), opts['ioForm']) > firstDayOfWeek

		for currentLine in reversed(linesFromFile):
			currentLine = currentLine.strip()
			if currentLine:
				time_str = currentLine[4:]
				state = currentLine[0]
				time = datetime.strptime(time_str, opts['ioForm'])
				if state == "i":
					if lastState == "o":
						totalTime += (lastTime - time).total_seconds()
				elif state == "o":
					lastTime = time
			else:
				state = "n"
			lastState = state
			lastTime = time
			if datetime.strptime(time_str, opts['ioForm']) < firstDayOfWeek: break

		if addCurrentTime:
			totalTime += (datetime.now() - datetime.strptime(linesFromFile[-1][4:].strip(), opts['ioForm'])).total_seconds()
		userFile.close()
		return totalTime
	except FileNotFoundError:
		#print('User '+n+"'s time file not found.")
		return 0

def calcSeasonHours(n):
	n = n.replace(' ','') # filenames have no spaces

	currentDate = datetime.now()
	buildStart = datetime.strptime(opts['buildStart'], opts['ioForm'])
	buildLeave = datetime.strptime(opts['buildLeave'], opts['ioForm'])

	buildDelta = currentDate-buildStart

	weeksSinceStart = max(buildDelta.days,0)

	if not ( buildStart <= currentDate <= buildLeave ): return calcWeekTime(n),0 # if not in build season, just give the total hours for this week

	totalTime = 0
	lastTime = 0
	lastState = 'n'

	try:
		with open(opts['pathTime'] + n + '.txt', 'r') as f: userIOAs = f.readlines()

		addCurrentTime = userIOAs and userIOAs[-1][0]=='i' and datetime.strptime(userIOAs[-1][4:].strip(), opts['ioForm']) > currentDate

		for line in reversed(userIOAs):
			line = line.strip()
			if line:
				time_str = line[4:]
				state = line[0]
				time = datetime.strptime(time_str, opts['ioForm'])
				if state == "i":
					if lastState == "o": totalTime += (lastTime - time).total_seconds()
				elif state == "o":
					lastTime = time
			else:
				state = "n"
			lastState = state
			lastTime = time
			if datetime.strptime(time_str, opts['ioForm']) < buildStart:
				#print(n+"'s done ", totalTime)
				break

		if addCurrentTime: totalTime += (currentDate - datetime.strptime(userIOAs[-1][4:].strip(), opts['ioForm'])).total_seconds()

		return totalTime, weeksSinceStart
	except FileNotFoundError:
		return 0, weeksSinceStart
#print('Days Since Start :', ( datetime.now()-datetime.strptime(opts['buildStart'], opts['ioForm']) ).days)
#print('Weeks Since Start:', ( datetime.now()-datetime.strptime(opts['buildStart'], opts['ioForm']) ).days//7)


def mkfile(t):
	open(t, 'a+').close()  # make files if they dont exist
