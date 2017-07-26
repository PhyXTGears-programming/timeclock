"""
Graphics.py

Support module providing all the graphics for the time clock.
"""

import ctypes
import turtle
from importlib import reload


class Graphics:

	machine_screen_width = ctypes.windll.user32.GetSystemMetrics(0)
	machine_screen_height = ctypes.windll.user32.GetSystemMetrics(1)

	def __init__(self,
				 title="Graphics Window",
				 bgColor="white",
				 screen={"width": 0.5,
						 "height": 0.5,
						 "startX": 0.5,
						 "startY": 0},
				 coordinates={"width": 1000,
							  "height": 1000,
							  "startX": 0,
							  "startY": 0}):
		self.buttons = []

		reload(turtle)
		self.t = turtle.Turtle(visible=False)
		self.s = turtle.Screen()

		self.s.tracer(False)
		self.s.title(title)
		self.s.screensize(bg=bgColor)
		self.setScreen(screen["width"],
					   screen["height"],
					   screen["startX"],
					   screen["startY"])
		self.setCoordinates(coordinates["width"],
							coordinates["height"],
							coordinates["startX"],
							coordinates["startY"])

	def setScreen(self,
				  scWidth=0.5,
				  scHeight=0.5,
				  scStartX=0.25,
				  scStartY=0.25):

		scWidth = int(scWidth * self.machine_screen_width)
		scHeight = int(scHeight * self.machine_screen_height)
		scStartX = int(scStartX * self.machine_screen_width)
		scStartY = int(scStartY * self.machine_screen_height)

		self.scHeight = scHeight
		self.s.setup(scWidth, scHeight, scStartX, scStartY)

	def setCoordinates(self,
					   wcWidth=1000,
					   wcHeight=1000,
					   wcX=0,
					   wcY=0):
		llx = wcX
		lly = wcY + wcHeight
		urx = wcX + wcWidth
		ury = wcY
		self.wcHeight = wcHeight
		self.s.setworldcoordinates(llx, lly, urx, ury)

	def getClick(self):
		self.s.onscreenclick(self.check)
		self.s.mainloop()
		return self.clickVal

	def check(self, x, y):
		for b in self.buttons:
			if ((b[0] < x < b[0] + b[2]) and
					(b[1] < y < b[1] + b[3])):
				self.clickVal = b[4]
				self.s.bye()

	def addButton(self, x, y, w, h, bColor, text, tColor, padding=20):
		self.buttons.append([x, y, w, h, text])

		self.t.penup()
		self.t.goto(x, y)
		self.t.pendown()
		self.t.fillcolor(bColor)
		self.t.begin_fill()
		for i in [w, h, w, h]:
			self.t.forward(i)
			self.t.left(90)
		self.t.end_fill()

		tX = x + (w / 2)

		pixelToUnitsRatio = self.scHeight / self.wcHeight
		boxInPixels = int(pixelToUnitsRatio * h)
		textSize = boxInPixels - (2 * padding)
		pixelShift = int(0.26378 * textSize + 3.3263)
		unitShift = int((pixelShift - padding) / pixelToUnitsRatio)
		tY = y + h + unitShift

		self.t.penup()
		self.t.goto(tX, tY)
		self.t.pendown()
		self.t.color(tColor)
		self.t.write(text, align='center', font=('Arial', textSize, 'bold'))
		self.t.color("black")
