# from https://github.com/Fantilein1990/vKeyboard
import tkinter as tk

class vk(tk.Frame):
	# --- A frame for the keyboard(s) itself --- #
	def __init__(self, parent, attach, keysize=4, enterAction=''):
		tk.Frame.__init__(self, takefocus=0)

		self.attach = attach
		self.keysize = keysize
		self.enterAction = enterAction

	# --- Different sub-keyboards (e.g. alphabet, symbols..) --- #
		# --- Lowercase alphabet sub-keyboard --- #
		self.alpha_Frame = tk.Frame(parent)
		self.alpha_Frame.grid(row=0, column=0, sticky="nsew")

		self.row1_alpha = tk.Frame(self.alpha_Frame)
		self.row2_alpha = tk.Frame(self.alpha_Frame)
		self.row3_alpha = tk.Frame(self.alpha_Frame)
		self.row4_alpha = tk.Frame(self.alpha_Frame)

		self.row1_alpha.grid(row=1)
		self.row2_alpha.grid(row=2)
		self.row3_alpha.grid(row=3)
		self.row4_alpha.grid(row=4)

		# --- Uppercase alphabet sub-keyboard --- #
		self.Alpha_Frame = tk.Frame(parent)
		self.Alpha_Frame.grid(row=0, column=0, sticky="nsew")

		self.row1_Alpha = tk.Frame(self.Alpha_Frame)
		self.row2_Alpha = tk.Frame(self.Alpha_Frame)
		self.row3_Alpha = tk.Frame(self.Alpha_Frame)
		self.row4_Alpha = tk.Frame(self.Alpha_Frame)

		self.row1_Alpha.grid(row=1)
		self.row2_Alpha.grid(row=2)
		self.row3_Alpha.grid(row=3)
		self.row4_Alpha.grid(row=4)

		# --- Symbols and numerals sub-keyboard --- #
		'''
		self.Symbol_Frame = tk.Frame(parent)
		self.Symbol_Frame.grid(row=0, column=0, sticky="nsew")

		self.row1_Symbol = tk.Frame(self.Symbol_Frame)
		self.row2_Symbol = tk.Frame(self.Symbol_Frame)
		self.row3_Symbol = tk.Frame(self.Symbol_Frame)
		self.row4_Symbol = tk.Frame(self.Symbol_Frame)

		self.row1_Symbol.grid(row=1)
		self.row2_Symbol.grid(row=2)
		self.row3_Symbol.grid(row=3)
		self.row4_Symbol.grid(row=4)
		'''

		# --- Initialize all sub-keyboards --- #
		self.keyState = 1
		self.init_keys()

		self.alpha_Frame.tkraise()

		self.pack()

	def init_keys(self):
		self.alpha = {
			'row1': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
			'row2': ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
			'row3': ['ABC', 'z', 'x', 'c', 'v', 'b', 'n', 'm'],
			'row4': ['-', '[ space ]', 'Bksp']
		}
		self.Alpha = {
			'row1': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
			'row2': ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
			'row3': ['abc', 'Z', 'X', 'C', 'V', 'B', 'N', 'M'],
			'row4': ['-', '[ space ]', 'Bksp']
		}
		self.Symbol = {
			'row1': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Bksp'],
			'row2': ['abc', '!', '"', '$', '%', '&', '/', '(', ')', '[', ']', '='],
			'row3': ['@', '-', '_', '?', '#', '*', '{', '}', ':', ';', 'ENTER'],
			'row4': ['<<<','+', '[ space ]', '.', ',', '>>>']
		}

		for i in range(1, 3):
			if i == 1:
				self.keyStyle = self.alpha
				self.row1 = self.row1_alpha
				self.row2 = self.row2_alpha
				self.row3 = self.row3_alpha
				self.row4 = self.row4_alpha
			elif i == 2:
				self.keyStyle = self.Alpha
				self.row1 = self.row1_Alpha
				self.row2 = self.row2_Alpha
				self.row3 = self.row3_Alpha
				self.row4 = self.row4_Alpha
			'''elif i == 3:
				self.keyStyle = self.Symbol
				self.row1 = self.row1_Symbol
				self.row2 = self.row2_Symbol
				self.row3 = self.row3_Symbol
				self.row4 = self.row4_Symbol'''

			for row in self.keyStyle.keys():  # iterate over dictionary of rows\
				f = 'Courier 16'
				if row == 'row1':  # TO-DO: re-write this method
					i = 1  # for readability and functionality
					for k in self.keyStyle[row]:
						c = lambda k=k: self._attach_key_press(k)
						if k == 'Bksp':
							tk.Button(self.row1, text=k, font=f, width=self.keysize*2, command=c).grid(row=0, column=i)
						else:
							tk.Button(self.row1, text=k, font=f, width=self.keysize, command=c).grid(row=0, column=i)
						i += 1
				elif row == 'row2':
					i = 2
					for k in self.keyStyle[row]:
						c = lambda k=k: self._attach_key_press(k)
						if k == 'Sym':
							tk.Button(self.row2, text=k, font=f, width=int(self.keysize*1.5), command=c).grid(row=0, column=i)
						elif k == 'abc':
							tk.Button(self.row2, text=k, font=f, width=int(self.keysize*1.5), command=c).grid(row=0, column=i)
						else:
							tk.Button(self.row2, text=k, font=f, width=self.keysize, command=c).grid(row=0, column=i)
						i += 1
				elif row == 'row3':
					i = 2
					for k in self.keyStyle[row]:
						c = lambda k=k: self._attach_key_press(k)
						if k == 'ABC':
							tk.Button(self.row3, text=k, font=f, width=int(self.keysize*1.5), command=c).grid(row=0, column=i)
						elif k == 'abc':
							tk.Button(self.row3, text=k, font=f, width=int(self.keysize*1.5), command=c).grid(row=0, column=i)
						elif k == 'ENTER':
							tk.Button(self.row3, text=k, font=f, width=int(self.keysize*2.5), command=c).grid(row=0, column=i)
						else:
							tk.Button(self.row3, text=k, font=f, width=self.keysize, command=c).grid(row=0, column=i)
						i += 1
				else:
					i = 3
					for k in self.keyStyle[row]:
						c = lambda k=k: self._attach_key_press(k)
						if k == '[ space ]':
							tk.Button(self.row4, text='	 ', font=f, width=self.keysize*6, command=c).grid(row=0, column=i)
						elif k == 'BACK':
							tk.Button(self.row4, text=k, font=f, width=self.keysize*2, command=c).grid(row=0, column=i)
						else:
							tk.Button(self.row4, text=k, font=f, width=self.keysize, command=c).grid(row=0, column=i)
						i += 1

	def _attach_key_press(self, k):
		if k == '>>>':
			self.attach.tk_focusNext().focus_set()
		elif k == '<<<':
			self.attach.tk_focusPrev().focus_set()
		elif k == 'Sym':
			self.Symbol_Frame.tkraise()
		elif k == 'abc':
			self.alpha_Frame.tkraise()
		elif k == 'ABC':
			self.Alpha_Frame.tkraise()
		elif k == 'Bksp':
			self.remaining = self.attach.get()[:-1]
			self.attach.delete(0, tk.END)
			self.attach.insert(0, self.remaining)
		elif k == 'ENTER':
			pass # Define, what's supposed to happen..
			#self.controller.enter_cb(self.enterAction)
		elif k == '[ space ]':
			self.attach.insert(tk.END, ' ')
		else:
			self.attach.insert(tk.END, k)
			
class vn(tk.Frame):
	#virtual numpad
	def __init__(self, parent, attach, keysize=4):
		tk.Frame.__init__(self,takefocus=0)
		self.attach = attach
		self.keysize = keysize
		
		self.numFrame = None
		
		self.init_keys()
		
		self.pack()