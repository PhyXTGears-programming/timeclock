import os
from tkinter import *
from ioService import *

root = Tk()
nuWin = None
fullnameEntry=usernameEntry=errorLabel = None
root.title('PhyxtGears1720io')
root.geometry('650x450')
'''
NOTES:
	check for files and folders at start of program
	add seperate sign in sign out buttons
	tabs for each team
	show hours in list.
	REORGANIZE IT ALL
'''

opts = {}
for line in open('opts.txt'): # load options
	line = line.strip().split(' : ')
	opts[line[0]] = line[1]

open(opts['usernameFile'],'a+').close()


def setScroll(*args):
	namelist.yview(*args)
	iolist.yview(*args)
def getNameFromListbox(): print(namelist.get(namelist.curselection()[0])) # return namelist.get(namelist.curselection()[0])

def quitNewUser():
	global nuWin
	nuWin.destroy()
	
def checkNameDB(n):
	for line in open(opts['usernameFile']):
		for item in line.split("|"):
			if item.lower() == n.lower(): return True
	return False
def finishNewUser():
	global nuWin
	global fullnameEntry,usernameEntry,errorLabel
	canerr,errmsg = True,'test error'
	
	if not checkNameDB(usernameEntry.get()): canerr,errmsg = True,'Err: Username already exists.'
	if not checkNameDB(fullnameEntry.get()): canerr,errmsg = True,'Err: Fullname already exists.'
	
	if not canerr:
		pass
	else:
		errorLabel.config(text=errmsg)
		
	print('Fullname: ',fullnameEntry.get())
	print('Username: ',usernameEntry.get())
def makeNewUserWindow():
	global nuWin
	global fullnameEntry,usernameEntry,errorLabel
	nuWin = Toplevel(root)
	nuWin.title('Create new user')
	nuWin.geometry('420x150')
	
	inputframe = Frame(nuWin)
	butonframe = Frame(nuWin)
	
	Label(inputframe, text='Fullname: ', font='Courier 12').grid(sticky=E,padx=2,pady=2)
	Label(inputframe, text='Username: ', font='Courier 12').grid(sticky=E,padx=2,pady=2)
	
	fullnameEntry = Entry(inputframe, font='Courier 12', width=30)
	usernameEntry = Entry(inputframe, font='Courier 12', width=30)
	fullnameEntry.grid(row=0,column=1)
	usernameEntry.grid(row=1,column=1)
	inputframe.pack()
	
	errorLabel = Label(nuWin, font='Courier 12', text='', fg='red')
	errorLabel.pack()
	
	finishButton = Button(butonframe, text='Create User',font='Courier 12', width=16, command=finishNewUser)
	cancelButton = Button(butonframe, text='Cancel',     font='Courier 12', width=16, command=quitNewUser)
	finishButton.grid(row=0,column=1)
	cancelButton.grid(row=0,column=0)
	butonframe.pack()
	

framelist = Frame(root)
scrolbar = Scrollbar(framelist, orient=VERTICAL)
namelist = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 12')
iolist   = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 12', justify=CENTER)

namelist.config(width=38,height=18)
iolist.config(width=1,height=18)
scrolbar.config(command=setScroll, width=52)

scrolbar.pack(side=RIGHT, fill=Y)
namelist.pack(side=LEFT, fill=BOTH, expand=1)
iolist.pack(side=LEFT, fill=BOTH, expand=1)
framelist.pack(side=LEFT)

logo1720 = PhotoImage(file='assets/logo.gif')
Label(root, text='PhyxtGears1720io', font='Courier 12').pack()
Label(root, image=logo1720).pack()

frameio = Frame(root)
innbutton = Button(frameio, text='IN',  font='Courier 12', command=getNameFromListbox, width=16, height=2)
outbutton = Button(frameio, text='OUT', font='Courier 12', command=getNameFromListbox, width=16, height=2)
newbutton = Button(frameio, text='New User', font='Courier 12', command=makeNewUserWindow, width=16, height=2)
innbutton.grid(row=0,pady=6)
outbutton.grid(row=1,pady=6)
newbutton.grid(row=2,pady=6)
frameio.pack()

for line in open(opts['usernameFile']):
	line = line.strip().split('|')
	namelist.insert(END, line[0])
	iolist.insert(END, 'N') #if random.random() >= 0.5: iolist.insert(END, 'o') else: iolist.insert(END, 'i')

root.mainloop()

#maingui()
#if __name__=='__main__': main()
