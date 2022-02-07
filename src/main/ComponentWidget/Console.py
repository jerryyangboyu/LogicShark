from PySide6.QtWidgets import QFrame, QWidget, QToolButton, QPushButton, QLineEdit, QTableWidget,  QTableWidgetItem
# ~ from PySide6.QtCore
from PySide6.QtGui import QIcon


class ConsoleWidget(QFrame):
	def __init__(self):
		super().__init__()
		self.setFixedHeight(200)
		self.setMinimumWidth(200)
		self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
		self.setAcceptDrops(True)
		self.setStyleSheet("background-color: #c02c38")
		
		# ~ self.buttonbox = []
		self.buttonSize = [40,40]
		self.bottonPosition = [10,10]
		self.space = 10
		self.bottonNumber = 1
		
		
		
		
		self.plusButton = QPushButton('+', self)
		self.plusButton.resize(self.buttonSize[0],self.buttonSize[1])
		self.plusButton.move(self.bottonPosition[0],self.bottonPosition[1])
		self.plusButton.clicked.connect(self.plusButtonHandle)
		
		
		# ~ self.tmpButton = QPushButton('+', self)
		# ~ self.bottonBox = [self.plusButton,self.tmpButton]
		self.currentBotton = self.plusButton
		
		self.currentLineEdit = QLineEdit('Enter your expression', self)
		self.currentLineEdit.resize(self.buttonSize[0]*6,self.buttonSize[1])
		self.lEXcord = self.bottonPosition[0]+self.buttonSize[0]+self.space/2
		self.currentLineEdit.move(self.lEXcord,self.bottonPosition[1])
		
		self.currentLineEdit.editingFinished.connect(self.currentLineEditHandle)
		

		
		
		
		
		
	def plusButtonHandle(self):
		self.currentBotton.setFlat(True)
		self.currentBotton.setText("Exp " + str(self.bottonNumber))
		self.createNewButton()
		
		
		
		
		
		
	def createNewButton(self):
		# ~ print(111111111)
		self.newButton = QPushButton('+', self)
		self.newButton.resize(self.buttonSize[0],self.buttonSize[1])
		
		newYCord = self.bottonPosition[1]+self.space+self.buttonSize[1]
		
		self.newButton.move(self.bottonPosition[0],newYCord)
		self.newButton.show()
		self.bottonNumber += 1
		
		
		# ~ self.newButton.clicked.connect(self.plusButtonHandle)
		
	# ~ def reName(self,botton):
	def currentLineEditHandle(self):
		text = self.currentLineEdit.text()
		self.translateExpr(text)
	
	
	
	def translateExpr(self,text):
		a = text.split(" ")
		unit1 = UnitExprssion(None,None,a[0])
		unit0 = UnitExprssion([None,None,a[0]],a[1],a[2])
		LE0 = LinkedExpression(unit1)
		LE0.append(unit0)
		self.createTruthTable(LE0)
		# ~ return a
		
		# ~ for i in text:
			# ~ if i.isAlpha() and 
			
	def createTruthTable(self,Exprs):
		column = Exprs.length()
		row = 2**Exprs.elemntsNumber()+1
		# ~ print (row)		
		self.truethTable = QTableWidget(row, column+row-1+1, self)
		self.truethTable.move(self.lEXcord+self.space+self.buttonSize[0]*6,self.bottonPosition[1])
		self.mapTable(Exprs,row,column)
		self.truethTable.show()
			
	def mapTable(self,Exprs,row,column):
		item = QTableWidgetItem()
		elmts = Exprs.elemnts()
		for i in range(len(elmts)):
			item.setText(elmts[i])
			self.truethTable.setItem(0, i+1, item)
		# ~ for i in range(column):
		item.setText("A && B")
		
		self.truethTable.setItem(3, 0, item)
		
		
		
	
			
			
			
			
			
			
			
			
			
			
class UnitExprssion():
	def __init__(self,A=None,operator=None,B=None):
		self.operator = operator
		self.A = A
		self.B = B			
	def isValue(self):
		return not self.operator
		
	def setValue(self,val):
		if self.A == None:
			self.A = val
		elif self.operator == None:
			self.operator = val
		else:
			self.B = val
	def __str__(self):
		return self.A + " " +self.operator+" "+self.B
		
		
	def setA(self,A):
		self.A = A
		
	def setOperator(self,A):
		self.operator = A
		
	def setB(self,A):
		self.B = A
		
		
		
			
class LinkedExpression():
	def __init__(self,unit =None,up=None,down=None):
		self.up = up
		self.val = unit
		self.down = down
		
	def append(self,downNode):
		
		if not self.down:
			downNode = LinkedExpression(downNode)
			self.down = downNode
			self.down.up = self
		else:
			self.down.append(downNode)
		
	# ~ def pop(self):
		# ~ self.down.up = None
		# ~ return self.val
		
	# ~ def setValue(self,val):
		# ~ self.val = val
		
	# ~ def createNewNode(self):
		# ~ return LinkedExpression()
	
	def length(self,sum = 0):
		sum += 1
		if self.down:
			return self.down.length(sum)
			
		return sum
		
	def elemntsNumber(self,elms = []):

		elms.append(self.val.B)
		if self.down:
			return self.down.elemntsNumber()
		return len(set(elms))
	def elemnts(self,elms = []):

		elms.append(self.val.B)
		if self.down:
			return self.down.elemnts()
		return list(set(elms))
			
		
		
	
		
		
		
		
		
		




