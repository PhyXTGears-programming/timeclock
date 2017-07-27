"""
myFunctions.py
A collaboration of funtions I've made that are useful for many programs

Functions:
	myInput
	myRound
"""


# A universal input function I use for many things
def myInput(message, errorMessage=None, strs=[], ints=[]):
	while True:
		I = input(message)
		if strs!=[] and I in strs: return I
		elif len(ints)==2 and I.isnumeric() and int(I)>=ints[0] and int(I)<=ints[1]: return int(I)
		elif strs == [] and ints == []: return I
		if errorMessage != None: print(errorMessage)


# A rounding function that actually works
def myRound(number, numDecimalPlaces):
	s = str(number)
	if "." in s:
		i = s.index(".")
		if len(s[i:]) > numDecimalPlaces: s = s[:i + numDecimalPlaces + 1]
	n = float(s)
	return n