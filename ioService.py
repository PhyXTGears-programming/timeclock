import os
import sys
import time
from datetime import datetime
from importlib import reload

from opts import opts

if not os.path.isdir(opts["path"]): os.mkdir(opts["path"])
open(opts['name.txt'], 'a').close() # create name file if it doesnt exist

def ioMain(n):
	complete = False
	if n=='new':
		name,user,jobo,an = '','','',' '
		print("\nEnter your full name. Ex: 'Bob Smith'.")
		while True: # Full name check
			name = input(':::> ')
			sp = name.split()
			if checkName(name): print('Err: Name already in database.')
			elif len(sp[0])<2: print('Err: First name too short.')
			elif not sp[0][0].isupper(): print('Err: First name needs to be capatalized.')
			elif len(sp)<2: print('Err: Full name required.')
			elif len(sp[1])<2: print('Err: Last name too short.')
			elif not sp[1][0].isupper(): print('Err: Last name needs to be capatalized.')
			else: break
		
		print("\nEnter your desired username. Ex: 'boboE512'.")
		while True: # Username check
			user = input(':::> ')
			if checkName(user): print('Err: Username already in database.')
			elif len(user)<4: print('Err: Username must be longer than 3 characters.')
			elif not (user.isalnum() or user.isalpha()): print('Err: Use letters and numbers only for username.')
			elif user.lower() in ['i','o','c','quit','admin','new']: print('Err: Username cannot be command.')
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
		print('Succesfully registered '+name+' as a'+an+jobo+' under '+user+'.')
		complete = True
	elif checkName(n):
		complete = True
		recordIO(getName(n),getIO())
	return complete

def checkName(n):
	for line in open(opts['name.txt']):
		#if n.lower() in line.lower(): return True
		for item in line.split("|"):
			if item.lower() == n.lower(): return True
	return False

def getName(n):
	for line in open(opts['name.txt']):
		for item in line.split("|"):
			if item.lower() == n.lower(): return line.split('|')[0]
	print('Err: Name not in database.')

def getIO():
	io = ''
	while True:
		print('\nAre you signing IN or OUT?')
		io = input(':::> ').lower()[0]
		if io in 'ioc': break
		else: print('Err: Invalid input.\n')
	return io

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
			cur = rl[-1].split()
			bck = rl[-2].split()
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
	print('Total hours: '+str(round(calcTotalTime(n)/3600, 2)))

def calcTotalTime(n): #returns total time in seconds
	total = 0
	iLin,oLin,tio = '','',0
	lastline = 'n'
	for line in open(opts['path']+n+'.txt'):
		if line[0]=='i' and lastline[0]!='i':
			iLin = line[4:-1]
		elif line[0]=='o' and lastline[0]!='o':
			oLin = line[4:-1]
			total = total + (datetime.strptime(oLin,opts['ioForm']) - datetime.strptime(iLin,opts['ioForm'])).total_seconds()
		lastline = line
	return total
	pass


def adminMain():
	admnpass = False
	while not admnpass:
		inpt = input('Passkey: ')
		if inpt==opts['adminPass']: admnpass=True
		elif inpt.lower() in ['cancel','quit']: break
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