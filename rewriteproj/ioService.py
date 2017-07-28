import os
import sys
import time

from opts import opts

if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])

def ioMain(n):
	if n=='new':
		name,user = '',''
		while True: # Full name check
			print("Enter your full name. Ex: 'Bob Smith'.")
			name = input(':::> ')
			if checkName(name): print('Err: Name already in database.\n')
			elif len(name.split()[0])<2: print('Err: First name too short.\n')
			elif len(name.split()[1])<2: print('Err: Last name too short.\n')
			elif name.find(' ')==-1: print('Err: No last name (no space).\n')
			elif not name.isalpha(): print('Err: Only use letters.\n')
			else: break
		while True: # Username check
			print("Enter your desired username. Ex: 'LogoE512'.")
			user = input(':::> ')
			if checkName(user): print('Err: 
			if len(user)<4: print('Err: Username must be longer than 3 characters.\n')
			elif user.find(' ')!=-1: print('Err: Cannot use spaces in username.')
			elif user.lower() in ['i','o','c','quit','admin','new']: print('Err: Username cannot be command.\n')
			
			else: break
	elif checkName(n):
	
	else:
		print('Err: Name not in database.\n')
	pass

def checkName(n):
	with open(opts['name.txt']) as f:
		for line in f:
			if n.lower() in line.lower():
				print(line)
				return True
	return False

def getName(n):
	pass

def getIO():
	io = ''
	while True:
		io = input('Are you signing IN or OUT? :::> ').lower()[0]
		if io in ['i','o','c']: break
		else: print('Invalid input.\n')
	return io


def adminMain():
	admnpass = False:
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
	print('\n'+'#'*50+'\n')
	print("Enter a Command or Username.\nType 'help' to show commands")
	while True:
		inpt = input(':::>')
		if len(inpt) < 3: print('Invalid input.')
		elif inpt=='help': pass
		elif inpt=='admin': adminMain()
		elif ioMain(inpt): pass
		elif inpt=='quit': break
		else: print('Invalid input.')

if __name__=='__main__':
	main()
	sys.exit(0)