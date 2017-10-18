import os
import time
import datetime
import sys
from platform import system
from tkinter import *
#from tkinter.ttk import *

from ioServ import *
import osk

root = Tk()
nuWin = None

# *F=frame, *S=scroll, *L=list, *B=button, *T=label, *E=entry
nuFullE = nuUserE = nuErrT = vkey = None
nameL = infoT = None

# root.config(bg='#000000')
root.title('PhyxtGears1720io')
root.geometry('800x600')  # 1024x768
if system() != 'Windows':
    root.attributes('-fullscreen', True)
'''
NOTES:
  tabs for each team (FLL and FIRST)
  show hours in list.
  REORGANIZE IT ALL
'''

opts = loadOpts()

try:
    os.mkdir(opts['pathTime'])
except:
    pass

open(opts['usernameFile'], 'a+').close()


def finishNewUser():
    global nuWin, nuFullE, nuUserE, nuErrT
    errmsg = 'no error'

    user = nuUserE.get()
    full = nuFullE.get()

    if user == '' or full == '':
        errmsg = 'Err: All boxes must be filled'
    elif checkNameDB(user):
        errmsg = 'Err: Username already exists.'
    elif checkNameDB(full):
        errmsg = 'Err: Fullname already exists.'

    if errmsg == 'no error':
        nuErrT.config(text='Making User\n-\nNo Error!', fg='green')
        addNameDB(full, user)  # todo: add job options
        refreshListboxes()
        nuWin.destroy()
    else:
        nuErrT.config(text=errmsg, fg='red')


def setVK(choice):
    global vkey, nuFullE, nuUserE
    # vkey.destroy()
    if choice == 1:
        vkey.attach = nuFullE
    elif choice == 2:
        vkey.attach = nuUserE


def quitNewUser():  # quit new user (dumb dank hack)
    global nuWin
    nuWin.destroy()


def makeNewUserWindow():  # new user window
    global root, nuWin
    global nuFullE, nuUserE, nuErrT, vkey

    nuWin = Toplevel(root)
    nuWin.title('Create new user')
    # nuWin.geometry('460x160')

    inputframe = Frame(nuWin)
    butonframe = Frame(nuWin)
    vkeyframe = Frame(nuWin, pady=8)

    Label(inputframe, text='Fullname: ', font='Courier 14').grid(sticky=E, padx=2, pady=2)
    Label(inputframe, text='Username: ', font='Courier 14').grid(sticky=E, padx=2, pady=2)

    nuFullE = Entry(inputframe, font='Courier 18', width=42)  # full name textbox
    nuUserE = Entry(inputframe, font='Courier 18', width=42)  # username  textbox

    nuFullE.bind('<FocusIn>', lambda e: setVK(1))
    nuUserE.bind('<FocusIn>', lambda e: setVK(2))

    nuFullE.grid(row=0, column=1)
    nuUserE.grid(row=1, column=1)
    inputframe.pack()

    nuErrT = Label(nuWin, font='Courier 14', text='', fg='red')  # if theres an error with the name (ie name exists or not a real name) show on screen
    nuErrT.pack()

    finishButton = Button(butonframe, text='Create User', font='Courier 14', fg='blue', width=16, command=finishNewUser)  # i hacked google
    cancelButton = Button(butonframe, text='Cancel',     font='Courier 14', fg='red',  width=16, command=quitNewUser)
    finishButton.grid(row=0, column=1)
    cancelButton.grid(row=0, column=0)
    butonframe.pack()

    vkey = osk.vk(parent=vkeyframe, attach=nuFullE)  # on screen alphabet keyboard
    vkeyframe.pack()


def refreshListboxes(n=None):
    global nameL, infoT
    if n == None:
        select = nameL.curselection()
        nameL.delete(0, END)
        sortUsernameList()

        nameIO = ''
        typeIO = 'N'

        for line in open(opts['usernameFile']):
            nameIO = line.strip().split('|')[0]
            try:
                with open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'r+') as f:
                    typeIO = f.readlines()[-1][0] #iolist.insert(END, f.readlines()[-1][0])
            except:
                typeIO = 'N'
            nameL.insert(END, nameIO+' '*(35-len(nameIO))+typeIO)

        if select: nameL.see(select[0])


def ioSign(c):
    global nameL, infoT
    if len(nameL.curselection()) == 0:
        infoT.config(text='Nothing Selected!', fg='red')
        return

    nameIO = nameL.get(nameL.curselection()[0])[:-1]
    timeIO = time.strftime(opts['ioForm'])
    autoClocked = False

    open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'a+').close()  # make file if it doesn't exist

    # REWRITE THIS WHOLE THING
    with open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'r+') as f:
        lines = [line.strip() for line in f]
        quitSign = False
        inTimeFrame = lines and lines[-1][0] == 'a' and datetime.strptime(lines[-1][4:], opts['ioForm']) < datetime.now() < datetime.now().replace(hour=4, minute=30, second=0, microsecond=0)
        if lines and c == 'o' and lines[-1][0] == 'a' and inTimeFrame:  # and datetime.now() < datetime.strptime(opts['autoClockLim'])
            nfile = open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'w+')
            nfile.write('\n'.join(lines[:-1]) + '\n')
            nfile.close()
            infoT.config(text=nameIO.split()[0] + ' signed out proper!', fg='Green')
            autoClocked = True
            # note for future annoucement system
            # have annoucements over phone system annoucing the time till autoclockout cutoff
            # "it is 4:00am, 1 hour till autoclockout cutoff. please be sure to sign out and sign back in to get the hours."
        elif lines and lines[-1][0] in 'ioa':
            if lines[-1][0] == 'i' and c == 'i':
                infoT.config(text=nameIO.split()[0] + ' is already signed in!', fg='orange')
                f.close()
                return
            elif lines[-1][0] in 'oa' and c == 'o':
                if lines[-1][0] == 'o':
                    infoT.config(text=nameIO.split()[0] + ' is already signed out!', fg='orange')
                elif lines[-1][0] == 'a':
                    infoT.config(text=nameIO.split()[0] + ' was auto-signed out!', fg='orange')
                f.close()
                return
        else:
            if not lines and c == 'o':
                infoT.config(text=nameIO.split()[0] + ' has never signed in!', fg='orange')
                f.close()
                return

    # note for out signio: even if there is an issue one signout, show an error but still log the out.
    # this was robby's idea
    file = open(opts['pathTime'] + nameIO.replace(' ', '') + '.txt', 'a+')
    file.write(c + ' | ' + timeIO + '\n')
    file.close()
    refreshListboxes()
    if not autoClocked:
        hours = str(round(calcTotalTime(nameIO.replace(' ', '')) / 60 / 60, 2))
        if c == 'i':
            infoT.config(text=nameIO.split()[0] + ' signed in! ' + hours + ' hours.', fg='Green')
        elif c == 'o':
            infoT.config(text=nameIO.split()[0] + ' signed out! ' + hours + ' hours.', fg='Red')


def confirmQuit(): # quit program window with passcode protection
    global root, opts
    qtWin = Toplevel(root)
    qtWin.title('Quit?')
    Label(qtWin, text='Enter AdminPass\nto quit.', font='Courier 16 bold').pack(pady=2)
    passEntry = Entry(qtWin, font='Courier 14', width=10, show='*')
    passEntry.pack(pady=2)

    def areYouSure():
        if passEntry.get() == opts['adminPass']: root.destroy()

    buttonF = Frame(qtWin)
    quitit = Button(buttonF, text='Quit',  font='Courier 14 bold', fg='red', command=areYouSure)
    cancit = Button(buttonF, text='Cancel', font='Courier 14 bold', fg='blue', command=qtWin.destroy)
    quitit.grid(column=0, row=0)
    cancit.grid(column=1, row=0)
    buttonF.pack(pady=2)
    vnum = osk.vn(parent=qtWin, attach=passEntry)


def main():
    # *F = frame, *S = scroll, *L = list, *B = button, *T = text
    global nameL, infoT
    listF = Frame(root)
    listS = Scrollbar(listF, orient=VERTICAL)
    nameL = Listbox(listF, selectmode=SINGLE, yscrollcommand=listS.set, font='Courier 18')
    nameL.config(width=36, height=20)
    listS.config(command=nameL.yview, width=52)

    listS.pack(side=RIGHT, fill=Y)
    nameL.pack(side=LEFT, fill=BOTH, expand=1)
    listF.pack(side=LEFT, padx=12)

    logo1720 = PhotoImage(file='assets/logo.gif')
    Label(root, text='PhyxtGears1720io', font='Courier 12').pack(pady=4)
    Label(root, image=logo1720).pack()

    ioF = Frame(root)
    iIOB = Button(ioF, text='IN',  font='Courier 16 bold', bg='green', fg='white', command=lambda: ioSign('i'), width=12, height=2)
    oIOB = Button(ioF, text='OUT', font='Courier 16 bold', bg='red',  fg='white',   command=lambda: ioSign('o'), width=12, height=2)
    infoT = Label(ioF, text='', font='Courier 16 bold', height=6, wraplength=192, justify=CENTER)
    newB = Button(ioF, text='New User', font='Courier 16 bold', bg='blue', fg='white', command=makeNewUserWindow, width=12, height=2)

    iIOB.pack(pady=4)
    oIOB.pack(pady=4)
    infoT.pack()
    newB.pack(pady=4)
    ioF.pack()

    Button(text='QUIT', font='Courier 16 bold', height=1, fg='red', command=confirmQuit).pack(side=RIGHT, padx=12)

    refreshListboxes()

    root.mainloop()


if __name__ == '__main__':
    main()
