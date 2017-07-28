import os
import sys
import time

from opts import opts

if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])

def ioMain(n):
	complete = False
	if n=='new':
		name,user,jobo = '','',''
		while True: # Full name check
			print("\nEnter your full name. Ex: 'Bob Smith'.")
			name = input(':::> ')
			if checkName(name): print('Err: Name already in database.')
			elif len(name.split()[0])<2: print('Err: First name too short.')
			elif len(name.split()[1])<2: print('Err: Last name too short.')
			elif name.find(' ')==-1: print('Err: No last name (no space).')
			# elif not name.isalpha(): print('Err: Only use letters.\n')  # allow certain characters like spaces and hyphens
			else: break
		while True: # Username check
			print("\nEnter your desired username. Ex: 'LogoE512'.")
			user = input(':::> ')
			if checkName(user): print('Err: Name already in database.')
			elif len(user)<4: print('Err: Username must be longer than 3 characters.')
			elif user.find(' ')!=-1: print('Err: Cannot use spaces in username.')
			elif user.lower() in ['i','o','c','quit','admin','new']: print('Err: Username cannot be command.')
			else: break
		while True:
			print('\nEnter a role. Ex: "s":student, "m":mentor, "a":adult.')
			jobo = input(':::> ')
			jobOpt = {'s':'student', 'm':'mentor', 'a':'adult'}
			if jobOpt[jobo.lower()[0]]:
				jobo = jobOpt[jobo.lower()[0]]
				break
			else:
				print('Err: Invalid input.')
		with open(opts['name.txt'],'a') as f: f.write(name+'|'+user+'|'+jobo+'\n')
		print('Succesfully registered '+name+' as a '+jobo+' under '+user+'.')
		complete = True
	elif checkName(n):
		complete = True
		n,io = getName(n),getIO()
		recordIO(n,io)
		pass
	return complete

def checkName(n):
	for line in open(opts['name.txt']):
		if n.lower() in line.lower(): return True
	return False

def getName(n):
	for line in open(opts['name.txt']):
		if n.lower() in line.lower(): return line.split('|')[0]
	print('Err: Name not in database.')

def getIO():
	io = ''
	while True:
		print('\nAre you signing IN or OUT?')
		io = input(':::> ').lower()[0]
		if io in ['i','o','c']: break
		else: print('Err: Invalid input.\n')
	return io

def recordIO(n,io):
	timeIO = time.strftime('%H:%M:%S')
	dateIO = time.strftime('%a.%b.%d.%Y')
	if io=='c':
		return
	elif io=='i':
		pass
	elif io=='o':
		pass
	
	with open(opts['path']+n+'.txt','a') as f: f.write(io.upper()+' | '+timeIO+' | '+dateIO+'\n')
	print(io.upper()+' | '+timeIO+' | '+dateIO)
	pass


def adminMain():
	admnpass = False
	while True:
		inpt = input('Passkey: ')
		if inpt==opts['adminPass']: admnpass=True
		elif inpt in ['cancel','quit','Cancel','Quit']: break
		else: print('Invalid input.')
	while admnpass:
		print('\n'*50)
		inpt = input(':::>')
		break # or admnpass = False
	pass # work on this i guess


def main():
	while True:
		print('\n'+'#'*78+'\n')
		print("Enter a Command or Username.\nType 'help' to show commands")
		inpt = input(':::> ')
		if len(inpt) < 3: print('Invalid input.')
		elif inpt=='help': pass
		elif inpt=='admin': adminMain()
		elif ioMain(inpt): pass
		elif inpt=='quit': break
		else: print('Err: Invalid input.')

if __name__=='__main__':
	main()
	sys.exit(0)