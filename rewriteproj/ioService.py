import os
import sys
import time

from opts import opts

if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])

def ioMain(n):
	if n=='new':
		name = input('')
	pass

def checkName(n):
	with open(opts['name.txt']) as f:
		for line in f:
			if n in line:
				print(line)
				return True
	return False

def getName(n):
	pass

def getIO():
	while True:
		io = input('Are you signing IN or OUT? :::> ')
		if io in ['in','IN','i','I']: io = 'i'
		elif io in ['out','OUT','o','O']: io = 'o'
		elif io in ['cancel','CANCEL']: io = 'c'
		else: print('Invalid input.\n')
	pass


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
		break
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