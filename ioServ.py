import imp
import os
import sys
from datetime import datetime

# if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])
# open(opts['name.txt'], 'a').close() # create name file if it doesnt exist


def loadOpts():
    opts = {}
    os.chdir(os.path.dirname(__file__))
    for line in open('opts.txt'):  # load options
        line = line.split("#")[0].strip().strip(" ")
        if line and line[0] != "#":
            line = line.strip().split(' : ')
            opts[line[0]] = line[1].split('#')[0].strip(' ')
    return opts


opts = loadOpts()


def checkNameDB(n):  # check for if a name exists already
    for line in open(opts['usernameFile']):
        for item in line.split("|"):
            if item.lower().replace(' ', '') == n.lower().replace(' ', ''):
                return True
    return False


def addNameDB(full, user, job=''):  # add a new name to the list
    file = open(opts['usernameFile'], 'a+')
    file.write(full.title() + '|' + user.title() + '\n')  # full+'|'+user+'|'+job+'\n'
    file.close()


def sortUsernameList():  # alphebetize names
    with open(opts['usernameFile']) as u:
        names = [x.title() for x in u.readlines()]
        names.sort()
    with open(opts['usernameFile'], 'w') as f:
        f.write(''.join(names))


def impFile(libPath):
    # sys.path.insert(0, os.path.abspath(libPath))
    # print(os.path.abspath(libPath))
    # print(sys.path)
    mod_name, file_ext = os.path.splitext(os.path.split(os.path.abspath(libPath + "mainHours.py"))[-1])
    imp.load_source(mod_name, os.path.abspath(libPath + "mainHours.py"))


def calcTotalTime(n):  # returns total time in seconds
    libPath = loadOpts()["hoursLocation"]
    if libPath == "enterLoationOf_timeclock-hours":
        total = 0
        iLin, oLin = '', ''
        prev = 'n'
        for line in open(opts['pathTime'] + n + '.txt'):
            line = line.strip()
            lastIOA = prev[0]
            currIOA = line[0]

            if currIOA == 'i':
                iLin = line[4:]
            elif currIOA == 'o' and lastIOA != 'o' and iLin != '':
                oLin = line[4:]
                total = total + (datetime.strptime(oLin, opts['ioForm']) - datetime.strptime(iLin, opts['ioForm'])).total_seconds()
            prev = line
        return total
    else:
        impFile(libPath)
        return mainHours.getSecs(opts['pathTime'] + n + '.txt')


def getTimeString(path):
    libPath = loadOpts()["hoursLocation"]
    if libPath == "enterLoationOf_timeclock-hours":
        hours = str(round(calcTotalTime(path) / 60 / 60, 2))
        return ' ' + hours + ' hours.'
    else:
        impFile(libPath)
        secs = calcTotalTime(path)
        return '\n' + mainHours.formatTime(secs)


def mkfile(t):
    open(t, 'a+').close()  # make files if they dont exist


'''
def recordIO(n,io):
	file = open(opts['path']+n+'.txt', 'a+') # create file if it doesnt exist
	timeIO = time.strftime(opts['ioForm'])
	writ = io+' | '+timeIO+'\n'
	# print(open(opts['path']+n+'.txt').readlines()[-1])

	if io=='c':
	return
	elif io=='i':
	pass
	elif io=='o':
	fintry = False
	try:
		rl = open(opts['path']+n+'.txt').readlines()
		cur,bck = rl[-1].split(),rl[-2].split()
		if cur[2]==bck[2] and cur[3]==bck[3]:
		del rl[-1]
		open(opts['path']+n+'.txt', 'w').write('\n'.join(rl))
		fintry = True
	except:
		pass
	if not fintry:
		rl = open(opts['path']+n+'.txt').readlines()
		if rl and rl[-1][0]!="i":
		print("Didn't sign in!")
		return

	file.write(writ)
	file.close()
	print('Total hours: '+str(round(calcTotalTime(n)/3600,1)))
def getIO():
	io = ''
	while True:
	print('\nAre you signing IN or OUT?')
	io = input(':::> ').lower()[0]
	if io in 'ioc': break
	else: print('Err: Invalid input.\n')
	return io
def ioMain(n):
	complete = False
	namefound = checkName(n)
	if n=='new':
	name,user,jobo,an = '','','',' '
	print("\nEnter your full name. Ex: 'Bob Smith'.")
	while True: # Full name check
		name = input(':::> ').title()
		sp = name.split()
		if checkName(name): print('Err: Name already in database.')
		elif len(sp[0])<2: print('Err: First name too short.')
		elif len(sp)<2: print('Err: Full name required.')
		elif len(sp[1])<2: print('Err: Last name too short.')
		else: break

	print("\nEnter your desired username. Ex: 'boboE512'.")
	while True: # Username check
		user = input(':::> ')
		if checkName(user): print('Err: Username is taken.')
		elif len(user)<4: print('Err: Username must be longer than 3 characters.')
		elif not (user.isalnum() or user.isalpha()): print('Err: Use letters and numbers only for username.')
		elif user.lower() in ['quit','admin']: print('Err: Username cannot be command.')
		else: break

	print('\nEnter a role.')
	for i,v in opts['roles'].items(): print(i+'. '+v)
	while True:
		jobo = input(':::> ')
		try:
		jobo = opts['roles'][jobo[0]]
		break
		except KeyError:
		print('Err: Invalid input.')
	with open(opts['name.txt'],'a') as f: f.write(name+'|'+user+'|'+jobo+'\n')
	if jobo[0] in 'aeiou': an='n '
	print('Succesfully registered '+name+' as a'+an+jobo+' with username '+user+'.')
	complete = True
	elif namefound:
	complete = True
	recordIO(getName(n),getIO())
	elif not namefound:
	print('Err: Name not found in database.')
	return complete
def main():
	while True:
	print('\n'+'#'*78+'\n')
	print("Enter a registered username or new to register a user.\nType '!help' to show commands")
	inpt = input(':::> ')
	if inpt=='quit': break
	elif inpt=='': print('Err: Please enter something.')
	elif inpt[0]=='!': pass
	elif ioMain(inpt): pass
'''

# if __name__=='__main__': main()
