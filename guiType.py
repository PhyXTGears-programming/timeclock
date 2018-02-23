import os, time
from time import strftime
from platform import system as platformsystem
from math import floor
from datetime import datetime,timedelta
from tkinter import *

import ioServ
import osk

root = Tk() # main window
nuWin = None # new user window
qtWin = None # quit password window

# *F=frame, *S=scroll, *L=list, *B=button, *T=label, *E=entry
nameL = infoT = logoImgs = logoL = None
logoCurrent = -1 # start on 0, since updateLogo adds 1

root.title('PhyxtGears1720io')
root.geometry('1024x768')  # 1024x768 # set resolution
glblBGC = '#343d46'
root.config(bg=glblBGC)
if platformsystem() != 'Windows' and platformsystem() != 'Darwin':
	root.attributes('-fullscreen', True)

opts = ioServ.loadOpts() # load options from file

try: os.mkdir(opts['pathTime'])
except FileExistsError: pass # but its a dir not a file

ioServ.mkfile(opts['usernameFile'])


allusers = {'all':[],'info':{}}
jobusers = {'none':[]}
for i in opts['posTitle']: allusers[i] = []
for i in opts['posJobs']:  jobusers[i] = []

for name in open(opts['usernameFile']):
	name = name.strip().split(" | ")
	allusers['all'].append(name[0])
	allusers[name[2]].append(name[0])
	for x in name[3].split(","):
		jobusers[x.strip()].append(name[0])
	allusers["info"][name[0]] = {"initials":name[1],"title":name[2],"jobs":name[3]}


	
def makeNewUserWindow():  # new user window
	global root, nuWin
	if nuWin != None and Toplevel.winfo_exists(nuWin): return

	nuWin = Toplevel(root) # make window
	nuWin.attributes('-topmost',1)
	nuWin.title('Create new user')
	#nuWin.geometry('460x160')

	inputF = Frame(nuWin) # frame for input boxes
	buttnF = Frame(nuWin) # frame for buttons
	titleF = Frame(nuWin) # frame for choosing between student mentor or adult
	jobsF  = Frame(nuWin) # frame for choosing the jobs you have
	vkeyF = Frame(nuWin, pady=8) # on screen keyboard frame

	Label(inputF, text='Fullname: ', font='Courier 14').grid(sticky=E, padx=2, pady=2)
	Label(inputF, text='Initials: ', font='Courier 14').grid(sticky=E, padx=2, pady=2)

	nuFullE = Entry(inputF, font='Courier 18', width=42)  # full name textbox
	nuUserE = Entry(inputF, font='Courier 18', width=42)  # username  textbox

	def setVK(choice): # function to set which input box the virtual keyboard puts text in
		if   choice == 1: vkey.attach = nuFullE
		elif choice == 2: vkey.attach = nuUserE
	nuFullE.bind('<FocusIn>', lambda e: setVK(1))
	nuUserE.bind('<FocusIn>', lambda e: setVK(2))

	nuFullE.grid(row=0, column=1)
	nuUserE.grid(row=1, column=1)
	inputF.pack()

	nuErrT = Label(nuWin, font='Courier 14', text='', fg='red')  # if theres an error with the name (ie name exists or not a real name) show on screen
	nuErrT.pack()

	# the different titles a member can have, like student mentor or adult
	titleOption, j = opts['posTitle'], 0
	titleChoice = IntVar(); titleChoice.set(0)
	for title in titleOption: # generate an option for every title in titleOption
		Radiobutton(titleF,text=title,font='Courier 14 bold', variable=titleChoice,value=j).grid(row=0,column=j)
		j += 1
	titleF.pack()

	#the different jobs a member can have, like programmer, mechanic, and/or media
	jobsOption, j = opts['posJobs'], 0
	jobsChoice = []
	for jobs in jobsOption: # generate an option for every jobs in jobsOption
		jobsChoice += [IntVar()]; jobsChoice[j].set(0)
		Checkbutton(jobsF,text=jobs,font='Courier 14 bold', variable=jobsChoice[j]).grid(row=0,column=j)
		j += 1
	jobsF.pack()


	def finishNewUser(): # perform checks on names for when the user is finished
		errmsg, user, full = 'None', nuUserE.get(), nuFullE.get()

		if user == '' or full == '': errmsg = 'Error: All boxes must be filled'
		elif ioServ.checkNameDB(full): errmsg = 'Error: Fullname already exists.'
		elif ioServ.checkNameDB(user): errmsg = 'Error: Username already exists.'

		if errmsg == 'None':
			jobsChosen,v = [],0
			for i in jobsChoice:
				if i.get()==1: jobsChosen += [jobsOption[v]]
				v+= 1
			if not jobsChosen: jobsChosen = ['none']
			ioServ.addNameDB(full.title(), user.lower(), titleOption[titleChoice.get()], ','.join(jobsChosen))
			refreshListboxes()
			alertWindow(text='Make sure you, '+full.title()+', sign in!', fg='orange')
			nuWin.destroy()
		else:
			nuErrT.config(text=errmsg, fg='red')

	Button(buttnF, text='Cancel',      font='Courier 14', fg='red',  width=16, command=nuWin.destroy).grid(row=0, column=0)
	Button(buttnF, text='Create User', font='Courier 14', fg='blue', width=16, command=finishNewUser).grid(row=0, column=1)
	buttnF.pack()

	vkey = osk.vk(parent=vkeyF, attach=nuFullE)  # on screen alphabet keyboard
	vkeyF.pack()


def refreshListboxes(n=None): # whenever someone signs in/out or theres a new user
	global nameL, infoT

	def __addtolistbox(nameIO,select):
		try:
			with open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'r') as f:
				inSeason = False
				timet = 0
				for season in opts["seasons"]:
					v = ioServ.calcSeasonTime(nameIO, season)
					inSeason, timet = v[0],v[1]
					timet = min( int(timet//3600), 999 )
					if inSeason: break
				else:
					timet = min( int(ioServ.calcTotalTime(nameIO)//3600), 999 )
				timeIO = ' '*max(3-len(str(timet)),0) + str( timet )
				try:
					typeIO = f.readlines()[-1][0]
				except IndexError:
					typeIO = 'N'
		except FileNotFoundError:
			#print("couldnt find "+nameIO+"'s file")
			timeIO = '   '
			typeIO = 'N'
		weektime = floor(min(ioServ.calcWeekTime(nameIO)//3600,8))
		#print(nameIO, ioServ.calcWeekTime(nameIO)/3600)
		nameL.insert(select, nameIO + ' ' * (30 - len(nameIO)-4)+ ('.'*weektime + ' '*(8-weektime)) + '  ' + timeIO + '  ' + typeIO)
		nameL.itemconfig(select, {'fg' : hoursToColor(nameIO)})


	ioServ.sortUsernameList()

	allusers = {'all':[],'info':{}}
	jobusers = {'none':[]}
	for i in opts['posTitle']: allusers[i] = []
	for i in opts['posJobs']:  jobusers[i] = []

	for name in open(opts['usernameFile']):
		name = name.strip().split(" | ")
		allusers['all'].append(name[0])
		allusers[name[2]].append(name[0])
		for x in name[3].split(","):
			jobusers[x.strip()].append(name[0])
		allusers["info"][name[0]] = {"initials":name[1],"title":name[2],"jobs":name[3]}


	if n=='all' or n==None:
		nameL.delete(0, END)
		ioServ.sortUsernameList()

		nameIO = ''
		select = 0

		for name in allusers['all']:
			#nameIO = line.strip().split(' | ')[0]
			#print(nameIO)
			__addtolistbox(name, select)
			select += 1

	elif n=='single':
		select = nameL.curselection()[0]
		nameIO = nameL.get(select)[:-18].strip()
		nameL.delete(select,select)
		__addtolistbox(nameIO, select)
		nameL.see(select+1)

def hoursToColor(name):
	inSeason = False
	timet = 0
	days = 0
	for season in opts["seasons"]:
		inSeason, timet, days = ioServ.calcSeasonTime(name, season)
		if inSeason: break
	else:
		timet, days = ioServ.calcWeekTime(name),0

	timet /= 3600

	if timet >= 52: # light gray, done with hours
		return '#e0e0e0'

	if days > 7:
		days -= 7
		timet -= days*8/7 # in season

	if timet >= 6.0: return '#00bf00' # green
	elif timet >= 2: return '#FFAF00' # yellow orange
	else: return '#FF4444' # red

	return '#000000'



def ioSign(c):
	global nameL
	if len(nameL.curselection()) == 0:
		alertWindow(text='No name selected!', fg='orange')
		return

	msg,color = ioServ.signIO(nameL.get(nameL.curselection()[0])[:-18],c)
	alertWindow(text=msg, fg=color)

	refreshListboxes('single')



def alertWindow(text='',fg='orange',font='Courier 14 bold'):
	wind = Toplevel(root) # new window
	wind.geometry('320x120') # set resolution
	wind.overrideredirect(1) # make window borderless

	# add text to window
	Label(wind, text=text,fg=fg,font=font,height=6,wraplength=300,justify=CENTER).place(x=160,y=60,anchor=CENTER)

	wind.after(3000, wind.destroy) # exit window after 3 seconds



def confirmQuit():  # quit program window with passcode protection
	global root, opts, qtWin
	if qtWin != None and Toplevel.winfo_exists(qtWin): return
	qtWin = Toplevel(root)
	qtWin.title('Quit?')
	Label(qtWin, text='Enter AdminPass\nto quit.', font='Courier 16 bold').pack(pady=2)
	passEntry = Entry(qtWin, font='Courier 14', width=10, show='*')
	passEntry.pack(pady=2)

	def areYouSure():
		if passEntry.get() == opts['adminPass']:
			root.destroy()

	buttonF = Frame(qtWin)
	quitit = Button(buttonF, text='Quit',  font='Courier 14 bold', fg='red', command=areYouSure)
	cancit = Button(buttonF, text='Cancel', font='Courier 14 bold', fg='blue', command=qtWin.destroy)
	quitit.grid(column=0, row=0)
	cancit.grid(column=1, row=0)
	buttonF.pack(pady=2)
	vnum = osk.vn(parent=qtWin, attach=passEntry)

def updateLogo():
	global logoImgs, logoL, logoCurrent
	logoCurrent += 1
	if logoCurrent >= len(logoImgs): logoCurrent = 0
	logoL.config(image=logoImgs[logoCurrent])
	root.after(5000,updateLogo)



def main():
	# *F = frame, *S = scroll, *L = list, *B = button, *T = text
	global nameL, infoT, logoImgs, logoL
	listF = Frame(root, bg=glblBGC)
	listS = Scrollbar(listF, orient=VERTICAL)
	nameL = Listbox(listF, selectmode=SINGLE, yscrollcommand=listS.set, font='Courier 22 bold', bg=glblBGC)
	nameL.config(width=42, height=20)
	listS.config(command=nameL.yview, width=52)

	form = 'Name' +' '*32+ 'hrs i/o'
	Label(listF, text=form, font='Courier 22 bold',anchor=W,justify=LEFT, fg='white',bg=glblBGC).pack(anchor=W)
	listS.pack(side=RIGHT, fill=Y)
	nameL.pack(side=LEFT, fill=BOTH, expand=1)
	listF.pack(side=LEFT, padx=12)

	logoImgs = [PhotoImage(file='assets/1720.gif'),PhotoImage(file='assets/30483-2.gif'),PhotoImage(file='assets/34416-4.gif')]
	Label(root, text='PhyxtGears1720io', font='Courier 12', fg='white',bg=glblBGC).pack(pady=4)
	logoL = Label(root, image=logoImgs[0], bg=glblBGC); logoL.pack()
	updateLogo()

	f = 'Courier 22 bold'
	ioF = Frame(root, bg=glblBGC)
	iIOB = Button(ioF, text='IN',  font=f, bg='green', fg='white', command=lambda:ioSign('i'), width=12, height=2)
	oIOB = Button(ioF, text='OUT', font=f, bg='red',   fg='white', command=lambda:ioSign('o'), width=12, height=2)

	whatSeason = "Off"
	for season in opts["seasons"]:
		if datetime.strptime(opts[season+'Start'],opts['ioForm']) <= datetime.now() <= datetime.strptime(opts[season+'Leave'],opts['ioForm']):
			whatSeason = season
			break
	infoT = Label(ioF, text="Currently\nin\n"+whatSeason+"\nSeason", fg="white", font=f, height=5, wraplength=200, justify=CENTER, bg=glblBGC) # white space generator ftw

	newB = Button(ioF, text='New User', font=f, bg= 'blue', fg='white', command=makeNewUserWindow, width=12, height=2)

	iIOB.pack(pady=8)
	oIOB.pack(pady=8)
	infoT.pack()
	newB.pack()
	ioF.pack()

	Button(text='QUIT',   font=f, bg='#44515e', fg='#ff6666', command=confirmQuit).pack(side=RIGHT, padx=12)
	Button(text='UPDATE', font=f, bg='#44515e', fg='orange',  command=lambda: refreshListboxes(), height=1).pack(side=RIGHT)

	refreshListboxes()

	root.mainloop()


if __name__ == '__main__':
	main()
