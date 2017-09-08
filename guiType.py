import os
from tkinter import *
#from tkinter.ttk import *
from ioService import *

root = Tk()
nuWin = None
fullnameEntry=usernameEntry=errorLabel = None
namelist=iolist=iotext = None
root.title('PhyxtGears1720io')
root.geometry('800x600')
root.attributes('-fullscreen',True)
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

try:
	os.mkdir(opts['pathTime'])
except:
	pass
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
			if item.lower().strip(' ') == n.lower().strip(' '): return True
	return False
def addNameDB(full,user,job=''):
	file = open(opts['usernameFile'], 'a+')
	file.write(full+'|'+user+'|'+job+'\n')
	file.close()
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
		namelist.insert(END, full)
		iolist.insert(END, 'N')
		nuWin.destroy()
	else:
		errorLabel.config(text=errmsg, fg='red')
		
	print('Fullname: ',fullnameEntry.get())
	print('Username: ',usernameEntry.get())
def makeNewUserWindow():
	global nuWin
	global fullnameEntry,usernameEntry,errorLabel
	nuWin = Toplevel(root)
	nuWin.title('Create new user')
	nuWin.geometry('460x160')
	
	inputframe = Frame(nuWin)
	butonframe = Frame(nuWin)
	
	Label(inputframe, text='Fullname: ', font='Courier 14').grid(sticky=E,padx=2,pady=2)
	Label(inputframe, text='Username: ', font='Courier 14').grid(sticky=E,padx=2,pady=2)
	
	fullnameEntry = Entry(inputframe, font='Courier 14', width=30)
	usernameEntry = Entry(inputframe, font='Courier 14', width=30)
	fullnameEntry.grid(row=0,column=1)
	usernameEntry.grid(row=1,column=1)
	inputframe.pack()
	
	errorLabel = Label(nuWin, font='Courier 14', text='', fg='red')
	errorLabel.pack()
	
	finishButton = Button(butonframe, text='Create User',font='Courier 14', width=16, command=finishNewUser)
	cancelButton = Button(butonframe, text='Cancel',     font='Courier 14', width=16, command=quitNewUser)
	finishButton.grid(row=0,column=1)
	cancelButton.grid(row=0,column=0)
	butonframe.pack()

def ioSignI():
	global namelist,iotext
	if len(namelist.curselection())==0:
		iotext.config(text='Nothing Selected!', fg='red')
		return
	nameIO = namelist.get(namelist.curselection()[0])
	timeIO = time.strftime(opts['ioForm'])
	file = open(opts['pathTime']+nameIO.strip(' ')+'.txt', 'a+')
	file.write('i | '+timeIO+'\n')
	file.close()
	iotext.config(text=nameIO.split()[0]+' signed in!', fg='Green')
def ioSignO():
	global namelist,iotext
	if len(namelist.curselection())==0:
		iotext.config(text='Nothing Selected!', fg='red')
		return
	nameIO = namelist.get(namelist.curselection()[0])
	timeIO = time.strftime(opts['ioForm'])
	file = open(opts['pathTime']+nameIO.strip(' ')+'.txt', 'a+')
	file.write('o | '+timeIO+'\n')
	file.close()
	iotext.config(text=nameIO.split()[0]+' signed out!', fg='Green')

framelist = Frame(root)
scrolbar = Scrollbar(framelist, orient=VERTICAL)
namelist = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 18')
iolist   = Listbox(framelist, selectmode=SINGLE, yscrollcommand=scrolbar.set, font='Courier 18', justify=CENTER)

namelist.config(width=46,height=24)
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
innbutton = Button(frameio, text='IN',  font='Courier 16 bold', command=ioSignI, width=12, height=2)
outbutton = Button(frameio, text='OUT', font='Courier 16 bold', command=ioSignO, width=12, height=2)
iotext = Label(frameio, text='', font='Courier 16 bold')
newbutton = Button(frameio, text='New User', font='Courier 16 bold', command=makeNewUserWindow, width=12, height=2)
innbutton.pack(pady=4)
outbutton.pack(pady=4)
iotext.pack()
newbutton.pack(pady=36)
frameio.pack()

Button(text='QUIT', font='Courier 16 bold', fg='red', command=root.destroy).pack()

#for x in range(100):
for line in open(opts['usernameFile']):
	line = line.strip().split('|')
	namelist.insert(END, line[0])
	iolist.insert(END, 'N')
	#if random.random() >= 0.5: iolist.insert(END, 'o') else: iolist.insert(END, 'i')

root.mainloop()

#maingui()
#if __name__=='__main__': main()
