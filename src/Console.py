from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QFrame, QWidget, QToolButton, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QVBoxLayout
# ~ from PySide6.QtCore
from PySide6.QtGui import QIcon


class CustomEditWidget(QLineEdit):
    inputChangeEvent = Signal(int)

    def __init__(self, content: str, lineEditId: int):
        super().__init__(content)
        self.lineEditId = lineEditId
        self.editingFinished.connect(self.internalFinishHandle)

    def internalFinishHandle(self) -> None:
        self.inputChangeEvent.emit(self.lineEditId)


class ConsoleWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.inputWidgets = []
        self.labelWidgets = []
        self.currentLineId = 0
        self.truthTable = QTableWidget()
        self.setFixedHeight(200)
        self.setMinimumWidth(200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        # self.setStyleSheet("background-color: #c02c38")

        self.currentExprNum = 0

        # Model
        self.labelList = ["Label 1", "Label 2"]
        self.exprList = ["Expr 1", "Expr 2"]

        self.mainLayout = QHBoxLayout()
        self.inputListLayout = QGridLayout()
        self.listLayout = QVBoxLayout()

        self.labelWidgets = [self.createLabelButton() for _ in range(len(self.labelList))]
        self.inputWidgets = [self.createInputBox(self.exprList[i], i) for i in range(len(self.exprList))]
        # View
        for i in range(len(self.labelList)):
            self.inputListLayout.addWidget(self.labelWidgets[i], i, 0)
            self.inputListLayout.addWidget(self.inputWidgets[i], i, 1)

        self.listLayout.addLayout(self.inputListLayout)
        self.listLayout.addWidget(self.createNewButton())

        self.mainLayout.addLayout(self.listLayout)
        self.translateExpr("A and B")
        self.mainLayout.addWidget(self.truthTable)

        self.setLayout(self.mainLayout)
        self.update()

        #
        #
        # self.buttonSize = [40, 40]
        # self.bottonPosition = [10, 10]
        # self.space = 10
        # self.bottonNumber = 1
        #
        # self.plusButton = QPushButton('+', self)
        # self.plusButton.resize(self.buttonSize[0], self.buttonSize[1])
        # # self.plusButton.move(self.bottonPosition[0], self.bottonPosition[1])
        # self.plusButton.clicked.connect(self.plusButtonHandle)
        #
        # # ~ self.tmpButton = QPushButton('+', self)
        # # ~ self.bottonBox = [self.plusButton,self.tmpButton]
        # self.currentBotton = self.plusButton

        # self.lEXcord = self.bottonPosition[0] + self.buttonSize[0] + self.space / 2
        # self.currentLineEdit.move(self.lEXcord, self.bottonPosition[1])

        # self.

    def addRecord(self):
        self.inputListLayout.addWidget(self.createLabelButton(), self.currentLineId - 1, 0)
        self.inputListLayout.addWidget(self.createInputBox(self.exprList[-1], self.currentLineId), self.currentLineId - 1, 1)
        # self.listLayout.setRowStretch(len(self.labelList) + 1, 10)
        # self.listLayout.update()
        # Map the Model into widgets

    def newInputBoxEvent(self):
        self.currentExprNum += 1
        self.currentLineId += 1
        self.labelList.append("Expr " + str(self.currentExprNum))
        self.exprList.append("Enter your expr")
        self.addRecord()
        # self.currentBotton.setFlat(True)
        # self.currentBotton.setText("Exp " + str(self.bottonNumber))
        # self.createNewButton()

    def createLabelButton(self):
        newButton = QPushButton("Expr " + str(self.currentExprNum))
        newButton.resize(40, 40)
        return newButton

    def createInputBox(self, content: str, inputId: int):
        currentLineEdit = CustomEditWidget(content, inputId)
        currentLineEdit.resize(240, 40)
        currentLineEdit.inputChangeEvent.connect(self.selectInputBoxChange)
        return currentLineEdit

    def selectInputBoxChange(self, lineId):
        self.currentLineId = lineId
        print(self.exprList[lineId])

    def createNewButton(self):
        newButton = QPushButton('+')
        newButton.resize(40, 40)
        newButton.clicked.connect(self.newInputBoxEvent)
        return newButton

    # ~ self.newButton.clicked.connect(self.plusButtonHandle)

    def translateExpr(self, text):
        a = text.split(" ")
        unit1 = UnitExprssion(None, None, a[0])
        unit0 = UnitExprssion([None, None, a[0]], a[1], a[2])
        LE0 = LinkedExpression(unit1)
        LE0.append(unit0)
        self.createTruthTable(LE0)

    # ~ return a

    # ~ for i in text:
    # ~ if i.isAlpha() and

    def createTruthTable(self, Exprs):
        column = Exprs.length()
        row = 2 ** Exprs.elemntsNumber() + 1
        # ~ print (row)
        self.truthTable = QTableWidget(row, column + row - 1 + 1, self)
        # self.truethTable.move(self.lEXcord + self.space + self.buttonSize[0] * 6, self.bottonPosition[1])
        self.mapTable(Exprs, row, column)

    def mapTable(self, Exprs, row, column):
        item = QTableWidgetItem()
        elmts = Exprs.elemnts()
        for i in range(len(elmts)):
            item.setText(elmts[i])
            self.truthTable.setItem(0, i + 1, item)
        # ~ for i in range(column):
        item.setText("A && B")

        self.truthTable.setItem(3, 0, item)


class UnitExprssion():
    def __init__(self, A=None, operator=None, B=None):
        self.operator = operator
        self.A = A
        self.B = B

    def isValue(self):
        return not self.operator

    def setValue(self, val):
        if self.A == None:
            self.A = val
        elif self.operator == None:
            self.operator = val
        else:
            self.B = val

    def __str__(self):
        return self.A + " " + self.operator + " " + self.B

    def setA(self, A):
        self.A = A

    def setOperator(self, A):
        self.operator = A

    def setB(self, A):
        self.B = A


class LinkedExpression():
    def __init__(self, unit=None, up=None, down=None):
        self.up = up
        self.val = unit
        self.down = down

    def append(self, downNode):

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

    def length(self, sum=0):
        sum += 1
        if self.down:
            return self.down.length(sum)

        return sum

    def elemntsNumber(self, elms=[]):

        elms.append(self.val.B)
        if self.down:
            return self.down.elemntsNumber()
        return len(set(elms))

    def elemnts(self, elms=[]):

        elms.append(self.val.B)
        if self.down:
            return self.down.elemnts()
        return list(set(elms))
