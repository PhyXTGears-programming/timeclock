import random
import os
from tkinter import *

from opts import *

def setScroll(*args):
	namelist.yview(*args)
	iolist.yview(*args)
def onSelect(): print(namelist.curselection(), iolist.curselection())

root = Tk()
root.geometry('450x650')
#root.resizeable(width=False,height=False)

logo1720 = PhotoImage(file='assets/logo.gif')
Label(root, text='PhyxtGears1720io', font='Courier 12').pack()
Label(root, image=logo1720).pack()

framelist = Frame(root)
scrolbar = Scrollbar(framelist, orient=VERTICAL)
namelist = Listbox(framelist, yscrollcommand=scrolbar.set, font='Courier 12')
iolist   = Listbox(framelist, yscrollcommand=scrolbar.set, font='Courier 12', justify=CENTER)

namelist.config(width=38,height=18)
iolist.config(width=1,height=18)
scrolbar.config(command=setScroll, width=52)

scrolbar.pack(side=RIGHT, fill=Y)
namelist.pack(side=LEFT, fill=BOTH, expand=1)
iolist.pack(side=LEFT, fill=BOTH, expand=1)

framelist.pack()

iobutton = Button(root, text='IO', font='Courier 12', command=onSelect, width=16, height=2)
iobutton.pack()

'''namelist.insert(END, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz?!'); iolist.insert(END, 'o')
for x in range(100):
	namelist.insert(END, str(x))
	if random.random() >= 0.5:
		iolist.insert(END, 'o')
	else:
		iolist.insert(END, 'i')'''
for x in range(10):
	for line in open(opts['name.txt']):
		line = line.strip().split('|')
		namelist.insert(END, line[0])
		if random.random() >= 0.5:
			iolist.insert(END, 'o')
		else:
			iolist.insert(END, 'i')

root.mainloop()

#if __name__=='__main__': main()
