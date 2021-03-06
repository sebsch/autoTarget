#!/usr/bin/env python3

''' autoTarget.py

Copyright: Sebastian Schmid <s0543196@htw-berlin.de>

License:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


intro = '''

*********************************************************
Ihre Regierung hat soeben den WAR OF SADNESS ausgerufen.
Deshalb ist es Ihre Aufgabe Soldat, traurige Smilies zu 
eliminieren!

Unser neuartiges Drohnenmodell hat leider noch einige 
Schwächen. 
Es kann traurige Smilies nicht genau erkennen.

Doch unsere Regierung ist gut, ja sie ist besser!

Aus diesem Grund hat sie sich in ihrer unendlichen 
Weisheit entschlossen, dass, auch wenn Traurigkeit
und die AXES OF TEARS keine Kompromisse zulassen,
unsere besten Männer zur Kontrolle des Waffensystemes
verantwortlich sind.

So ist es nun Ihre Aufgabe das hochmoderne und
extrem humanitäre Drohnensystem zu bedienen Soldat!

Dazu geben sie die kill decision mit SPACE,
alles andere erledigt unser Waffensystem autonom.

Doch denken Sie daran, dass unsere Regierung den 
Kampf ernst nimmt!
Lassen Sie 10 Feinde am Leben, so verlieren Sie 
ihre Privilegien und ihr Haus. 
Sie werden ohne Ehren aus Ihrem Dienst entlassen  
und selbst zum Feind unseren allmächtigen 
Großreiches erklärt.

Wenn Sie Ihre Aufgabe verstanden haben, drücken sie 
ENTER um den Dienst an der guten Sache zu beginnen.

*********************************************************
'''


outro = '''


*********************************************************
Ihre Regierung wurde gestürzt und für ihre Kriegs-
verbrechen angeklagt.

Eine unabhängige Kommission hat eine Untersuchung 
eingeleitet.
Diese ergab, dass sie im Rahmen Ihres Drohnen-
einsatzes %s Zivilisten, darunter Kinder, Frauen 
und Ärzte getötet haben.

	      	    ---------
	      	    GAME OVER
	      	    ---------

*********************************************************


Kampfdrohnen machen Töten zum Kinderspiel!
Es ist Ihre Entscheidung.
Lassen Sie es nicht zu!
http://drohnen-kampagne.de/ 


'''

import sys
from PyQt4 import QtGui, QtCore
from random import randint, seed
from math import e
try:
	from subprocess import Popen, PIPE
except:
	print("For Gamemusic you need subprocess + mplayer")


class GameFrame(QtGui.QWidget):
	def __init__(self):
		super(GameFrame, self).__init__()		
		self.initUI()
		self.initEngine()

	
	def initUI(self):
		self.setGeometry(300, 300, 400, 300)
		self.setFixedSize(400,300)
		self.setWindowTitle('autoTarget   --  flying with drones')
		self.logo = True		
		if self.logo == True:
			pix = QtGui.QPixmap("htwlogo.png")
			logo = QtGui.QLabel(self)
			logo.setPixmap(pix)
			logo.move(155,260)

		self.show()

	def initEngine(self):
		self.engine = GameEngine()
		self.Target = self.engine.getTarget()
		self.roundTimer = QtCore.QTimer()
		self.roundTimer.timeout.connect(self.reloadTarget)
		self.roundTimer.start(
			self.engine.gameTimer(self.engine.rounds))

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawBackground(event, qp)
		self.drawTarget(event, qp, self.Target[0], self.Target[1])
		qp.end()

	def drawBackground(self, event, qp):
		color = QtGui.QColor(0,0,0)
		color.setNamedColor('#d4d4d4')
		qp.setPen(color)
		
		qp.setBrush(QtGui.QColor(20,20,20))
		qp.drawRect(0,0,400,300)

	def drawTarget(self, event, qp, text, color):
		if color == 'ROT':
			qp.setPen(QtGui.QColor(250,0,0))
		else:
			qp.setPen(QtGui.QColor(0,250,0))
		qp.setFont(QtGui.QFont('Decorative', randint(14, 45)))
		qp.drawText(randint(20, 260), randint(40, 200), text)

		qp.setPen(QtGui.QColor(0,0,0))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(10,290, str(self.engine.enemiesFailed))

	def reloadTarget(self, trigger=False):
		if not trigger and self.Target[0] == ':(':
			self.engine.enemiesFailed += 1	
		if self.engine.enemiesFailed >= 10:
			self.endGame()
		self.engine.rounds += 1
		self.Target = self.engine.getTarget()
		self.roundTimer.start(
			self.engine.gameTimer(self.engine.rounds))
		self.repaint()

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Space:
			self.killTarget()

	def killTarget(self):
		if self.Target[0] == ':(':
			self.reloadTarget(trigger=True)
		else:
			self.engine.killedKitten += 1
			self.reloadTarget(trigger=True)

	def endGame(self):
		print(outro % self.engine.killedKitten)
		self.close()

	

class GameEngine:
	
	def __init__(self):
		self.enemiesFailed = 0
		self.killedKitten = 0
		self.rounds = 1
		self.target = [
			(':(', 'ROT'),
			(':)', 'GRUEN'),
			(':(', 'GRUEN'),
			(':)', 'ROT')]

	def getTarget(self):
		seed()
		return self.target[randint(0,3)]
	

	def gameTimer(self, x):
		return(int(1000*((2*e**(10/(x+4)))-1.6)))	

		
def main():

	print(intro)
	input()
	# load Widget
	app = QtGui.QApplication(sys.argv)
	gf = GameFrame()
	sys.exit(app.exec_() )
	
	

if __name__ == '__main__':
	try:
		Popen(['mplayer', './Unityfinal.mp3', '-quiet'], stdout=PIPE)
	except:
		print("Sorry no Sound available.")
	try:
		main()
	except KeyboardInterrupt:
		print("\n\nInfo: Abbruch durch Benutzer\n")
		print("Info: Programm wird beendet!")

