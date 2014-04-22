#! /usr/bin/env py(thon


"""
paint bezier curves
"""

from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy as np
from scipy.special import binom
import sys

def Bernstein(n,k):
	"""
	definen Bernstein function
	"""
	coeff = binom(n,k)
	def _poly(x):
		return coeff * x**k * (1-x)**(n-k)
	return _poly
def BezierCurve(points,number):
	print points
	N = len(points)
	t = np.linspace(0,1,num=number)
	curve = np.zeros((number,2))
	for i in range(N):
		curve += np.outer(Bernstein(N-1,i)(t),points[i])
	return curve
class PaintWidget(QtGui.QWidget):
	"""
	the widget for paint
	"""
	def __init__(self,parent=None):
		super(PaintWidget,self).__init__(parent)
		self.points = []
		self.update()
		self.bezierCurve = []
		# set the background color
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(),QtGui.QColor(207,240,158))
		self.setPalette(p)
	def _pushPoint(self,pt):
		self.points.append(pt)
		self.bezierCurve = BezierCurve(self.points,200)
	def _popPoint(self,pt):
		if pt in self.points:
			self.points.remove(pt)
	def mousePressEvent(self,mouseEvent):
		currPt = (mouseEvent.x(),mouseEvent.y())
		self._pushPoint(currPt)
		#print self.points
		self.update()
	def paintEvent(self,event):
		painter = QtGui.QPainter(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		self.drawControlLines(painter)
		self.drawBezierCurve(painter)
		self.drawControlPoints(painter)
		
	def drawControlPoints(self,painter):
		painter.setPen(QtCore.Qt.red)
		painter.setBrush(QtCore.Qt.cyan)
		for pt in self.points:
			# draw a circle to stand for a point
			painter.drawEllipse(pt[0]-3,pt[1]-3,6,6)
	def drawControlLines(self,painter):
		painter.setPen(QtCore.Qt.blue)
		n = len(self.points)
		for i in range(n-1):
			painter.drawLine(self.points[i][0],self.points[i][1],self.points[i+1][0],self.points[i+1][1])
	def drawBezierCurve(self,painter):
		pen = QtGui.QPen()
		pen.setColor(QtGui.QColor(168,219,168))
		pen.setWidth(3)
		pen.setStyle(QtCore.Qt.DashDotLine)
		painter.setPen(pen)
		if len(self.points) > 2:
			N = len(self.bezierCurve)
			for i in range(N-1):
				painter.drawLine(self.bezierCurve[i][0],self.bezierCurve[i][1],self.bezierCurve[i+1][0],self.bezierCurve[i+1][1])

	def sizeHint(self):
		"""
		overload sizeHint to decide default size
		"""
		return QtCore.QSize(500,500)


class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window,self).__init__()
		paintwidget = PaintWidget(self)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(paintwidget)
		self.setCentralWidget(paintwidget)
		
def main():
	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()