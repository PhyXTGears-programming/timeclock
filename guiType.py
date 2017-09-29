import os
import time
import sys
from platform import system
from tkinter import *
#from tkinter.ttk import *

from ioServ import *
import osk

root = Tk()
nuWin = None
fullnameEntry=usernameEntry=errorLabel=vkey = None
namelist=iolist=iotext = None
root.title('PhyxtGears1720io')
root.geometry('800x600') #1024x768
if system() != 'Windows': root.attributes('-fullscreen',True)
'''
NOTES:
	tabs for each team (FLL and FIRST)
	show hours in list.
	REORGANIZE IT ALL
'''

opts = loadOpts()

try: os.mkdir(opts['pathTime'])
except: pass

open(opts['usernameFile'],'a+').close()


def setScroll(*args):
	namelist.yview(*args)
	iolist.yview(*args)
	
def finishNewUser():
	global nuWin
	global fullnameEntry,usernameEntry,errorLabel
	errmsg = 'no error'
	
	user = usernameEntry.get()
	full = fullnameEntry.get()
	
	if user=='' or full=='': errmsg = 'Err: All boxes must be filled'
	elif checkNameDB(user): errmsg = 'Err: Username already exists.'
	elif checkNameDB(full): errmsg = 'Err: Fullname already exists.'
	
	if errmsg == 'no error':
		errorLabel.config(text='Making User\n-\nNo Error!', fg='green')
		addNameDB(full,user) # todo: add job options
		refreshListboxes()
		nuWin.destroy()
	else:
		errorLabel.config(text=errmsg, fg='red')
		
def setVK(choice):
	global vkey, fullnameEntry,usernameEntry
	#vkey.destroy()
	if choice==1:
		vkey.attach=fullnameEntry
	elif choice==2:
		vkey.attach=usernameEntry
def quitNewUser(): # quit new user (dumb dank hack)
	global nuWin
	nuWin.destroy()
def makeNewUserWindow(): # new user window
	global root,nuWin
	global fullnameEntry,usernameEntry,errorLabel,vkey
	
	nuWin = Toplevel(root)
	nuWin.title('Create new user')
	#nuWin.geometry('460x160')
	
	
	inputframe = Frame(nuWin)
	butonframe = Frame(nuWin)
	vkeyframe = Frame(nuWin, pady = 8)
	
	Label(inputframe, text='Fullname: ', font='Courier 14').grid(sticky=E,padx=2,pady=2)
	Label(inputframe, text='Username: ', font='Courier 14').grid(sticky=E,padx=2,pady=2)
	
	fullnameEntry = Entry(inputframe, font='Courier 18', width=42) # full name textbox
	usernameEntry = Entry(inputframe, font='Courier 18', width=42) # username  textbox
	
	fullnameEntry.bind('<FocusIn>', lambda e: setVK(1))
	usernameEntry.bind('<FocusIn>', lambda e: setVK(2))
	
	fullnameEntry.grid(row=0,column=1)
	usernameEntry.grid(row=1,column=1)
	inputframe.pack()
	
	errorLabel = Label(nuWin, font='Courier 14', text='', fg='red') # if theres an error with the name (ie name exists or not a real name) show on screen
	errorLabel.pack()
	
	finishButton = Button(butonframe, text='Create User',font='Courier 14', fg='blue', width=16, command=finishNewUser) #i hacked google
	cancelButton = Button(butonframe, text='Cancel',     font='Courier 14', fg='red',  width=16, command=quitNewUser)
	finishButton.grid(row=0,column=1)
	cancelButton.grid(row=0,column=0)
	butonframe.pack()
	
	vkey = osk.vk(parent=vkeyframe, attach=fullnameEntry) # on screen alphabet keyboard
	vkeyframe.pack()

def refreshListboxes(): # BADLY NEEDS OPTIMIZATIONS
	global namelist,iolist,iotext
	namelist.delete(0,END)
	iolist.delete(0,END)
	with open(opts['usernameFile'],'r') as u:
		names = u.readlines()
		names = [x.title() for x in names]
		names.sort()
	with open(opts['usernameFile'],'w') as f: f.write(''.join(names))
	for line in open(opts['usernameFile']):
		line = line.strip().split('|')[0]
		namelist.insert(END, line)
		try:
			with open(opts['pathTime']+line.replace(' ','')+'.txt','r+') as f:
				iolist.insert(END, f.readlines()[-1][0])
		except:
			iolist.insert(END, 'N')

def ioSign(c):
	global namelsit,iolist,iotext
	if len(namelist.curselection())==0:
		iotext.config(text='Nothing Selected!', fg='red')
		return
	
	nameIO = namelist.get(namelist.curselection()[0])
	timeIO = time.strftime(opts['ioForm'])
	
	open(opts['pathTime']+nameIO.replace(' ','')+'.txt', 'a+').close() # make file if it doesn't exist
	with open(opts['pathTime']+nameIO.replace(' ','')+'.txt', 'r+') as f:
		lines = f.readlines()
		try:
			if lines[-1][0]==c:
				if c=='i': iotext.config(text=nameIO.split()[0]+' is already signed in!', fg='red')
				elif c=='o': iotext.config(text=nameIO.split()[0]+' is already signed out!', fg='red')
				f.close()
				return
		except:
			if not lines: 
				iotext.config(text=nameIO.split()[0]+' has never signed in!', fg='red')
				f.close()
				return
		if lines and lines[-1].strip()[-1]=='a': pass

	file = open(opts['pathTime']+nameIO.replace(' ','')+'.txt', 'a+')
	file.write(c+' | '+timeIO+'\n')
	file.close()
	refreshListboxes()
	if c=='i': iotext.config(text=nameIO.split()[0]+' signed in!', fg='Green')
	elif c=='o': iotext.config(text=nameIO.split()[0]+' signed out!', fg='Green')
	pass

def confirmQuit():
	global root,opts
	qtWin = Toplevel(root)
	qtWin.title('Quit?')
	Label(qtWin,text='Enter AdminPass\nto quit.', font='Courier 16 bold').pack(pady=2)
	passEntry = Entry(qtWin,font='Courier 14',width=10,show='*')
	passEntry.pack(pady=2)
	
	def areYouSure():
		if passEntry.get()==opts['adminPass']: root.destroy()
	
	framebutton = Frame(qtWin)
	quitit = Button(framebutton,text='Quit',  font='Courier 14 bold',fg='red', command=areYouSure)
	cancit = Button(framebutton,text='Cancel',font='Courier 14 bold',fg='blue', command=qtWin.destroy)
	quitit.grid(column=0,row=0)
	cancit.grid(column=1,row=0)
	framebutton.pack(pady=2)
	vnum = osk.vn(parent=qtWin, attach=passEntry)
	

def main():
	global namelist,iolist,iotext
	framelist = Frame(root)
	scrolbar = Scrollbar(framelist, orient=VERTICAL)
	namelist = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 18')
	iolist   = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 18', justify=CENTER)

	namelist.config(width=35,height=20)
	iolist.config(width=1,height=18)
	scrolbar.config(command=setScroll, width=52)

	scrolbar.pack(side=RIGHT, fill=Y)
	namelist.pack(side=LEFT, fill=BOTH, expand=1)
	iolist.pack(side=LEFT, fill=BOTH, expand=1)
	framelist.pack(side=LEFT,padx=12)

	logo1720 = PhotoImage(file='assets/logo.gif')
	Label(root, text='PhyxtGears1720io', font='Courier 12').pack(pady=4)
	Label(root, image=logo1720).pack()

	frameio = Frame(root)
	innbutton = Button(frameio, text='IN',  font='Courier 16 bold', fg='green', command=lambda: ioSign('i'), width=12, height=2)
	outbutton = Button(frameio, text='OUT', font='Courier 16 bold', fg='red',   command=lambda: ioSign('o'), width=12, height=2)
	iotext = Label(frameio, text='', font='Courier 16 bold',height=6, wraplength=192, justify=CENTER)
	newbutton = Button(frameio, text='New User', font='Courier 16 bold', fg='blue', command=makeNewUserWindow, width=12, height=2)
	
	innbutton.pack(pady=4)
	outbutton.pack(pady=4)
	iotext.pack()
	newbutton.pack(pady=4)
	frameio.pack()

	Button(text='QUIT', font='Courier 16 bold', height=1, fg='red', command=confirmQuit).pack(side=RIGHT,padx=12)

	refreshListboxes()

	root.mainloop()
if __name__=='__main__': main()
