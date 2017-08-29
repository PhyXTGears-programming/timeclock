import random
import os
from tkinter import *

def setScroll(*args):
	namelist.yview(*args)
	iolist.yview(*args)
def onSelect(): print(namelist.curselection(), iolist.curselection())

root = Tk()
root.geometry('450x650')
#root.resizeable(width=False,height=False)

Label(root, text='PhyxtGears1720io').pack()

framelist = Frame(root)
scrolbar = Scrollbar(framelist, orient=VERTICAL)
namelist = Listbox(framelist, yscrollcommand=scrolbar.set, font='Courier 8')
iolist   = Listbox(framelist, yscrollcommand=scrolbar.set, font='Courier 8', justify=CENTER)

namelist.config(width=50,height=12)
iolist.config(width=2,height=12)
scrolbar.config(command=setScroll)

scrolbar.pack(side=RIGHT, fill=Y)
namelist.pack(side=LEFT, fill=BOTH, expand=1)
iolist.pack(side=LEFT, fill=BOTH, expand=1)

framelist.pack()

iobutton = Button(root, text='IO', command=onSelect, width=20, height=2)
iobutton.pack()

for x in range(100):
	namelist.insert(END, str(x))
	if random.random() >= 0.5:
		iolist.insert(END, 'o')
	else:
		iolist.insert(END, 'i')

root.mainloop()

#if __name__=='__main__': main()