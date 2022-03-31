from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QFrame, QWidget, QToolButton, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QGridLayout, QListWidget, QListWidgetItem, QVBoxLayout, QScrollArea
# ~ from PySide6.QtCore
from PySide6.QtGui import QIcon

from LogicTypes import ConsoleData
from fileHandling import launchWriter
from algorithm import cnf, dnf, simplify


class CustomEditWidget(QLineEdit):

    inputChangeEvent = Signal(int)
    inputEditedEvent = Signal(int)

    def __init__(self, content: str, line_id: int):
        super().__init__(content)
        self.line_id = line_id
        self.editingFinished.connect(self.internalFinishHandle)
        self.textEdited.connect(self.internalChangeHappenHandle)

    def internalFinishHandle(self) -> None:
        self.inputChangeEvent.emit(self.line_id)

    def internalChangeHappenHandle(self) -> None:
        self.inputEditedEvent.emit(self.line_id)


class CustomLabel(QPushButton):

    def __init__(self, label, line_id):
        super().__init__(label)
        self.isActive = False
        self.setBackGround()
        self.line_id = line_id

    def setActive(self, active: bool):
        self.isActive = active
        self.setBackGround()

    def setBackGround(self):
        self.setStyleSheet(
            "background-color: {0}; border: none; color: white".format("red" if self.isActive else "blue"))


class ConsoleWidget(QFrame):
    OnGraphFinished = Signal(object)
    DrawGraphCommand = Signal(list)
    ExpressionLoaded = Signal(list)
    SaveExpressions = Signal()

    def __init__(self):
        super().__init__()
        self.inputWidgets = []
        self.labelWidgets = []
        self.currentLineId = 0
        self.truthTable = QTableWidget()

        # self.setMaximumHeight(400)
        self.setMaximumHeight(300)
        self.setMinimumWidth(200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        # self.setStyleSheet("background-color: #c02c38")
        self.lineEditWidth = 240
        self.inputListWidgetLen = 40 * len(self.inputWidgets)

        self.currentExprNum = 1

        # Model
        self.labelList = ["A", "B"]
        self.exprList = ["A & B", "A | ~C"]

        self.mainLayout = QHBoxLayout()
        self.inputListLayout = QGridLayout()
        self.inputListWidget = QWidget()
        self.listLayout = QVBoxLayout()

        self.inputListLayout.setContentsMargins(0, 0, 0, 0)
        self.inputListLayout.setVerticalSpacing(1)
        self.inputListLayout.setHorizontalSpacing(1)

        self.labelWidgets = [self.createLabelButton(self.labelList[i], i) for i in range(len(self.labelList))]
        self.inputWidgets = [self.createInputBox(self.exprList[i], i) for i in range(len(self.exprList))]
        # View
        for i in range(len(self.labelList)):
            self.inputListLayout.addWidget(self.labelWidgets[i], i, 0)
            self.inputListLayout.addWidget(self.inputWidgets[i], i, 1)

        self.currentLineId += (len(self.labelList) - 1)

        self.inputListLayout.setColumnStretch(len(self.inputWidgets), 100)
        # ~ self.inputListLayout.setRowStretch(0, 10)

        self.scrollArea = QScrollArea()
        self.inputListWidget.setLayout(self.inputListLayout)
        self.inputListWidget.setMinimumHeight(40 * len(self.inputWidgets))
        self.scrollArea.setWidget(self.inputListWidget)

        self.listLayout.addWidget(self.scrollArea)

        self.listLayout.addWidget(self.createNewButton())

        self.mainLayout.addLayout(self.listLayout)
        self.mainLayout.addWidget(self.truthTable)

        self.setLayout(self.mainLayout)
        self.update()

        self.OnGraphFinished.connect(self.handleGraphComplete)
        self.ExpressionLoaded.connect(self.handleExpressionLoaded)
        self.SaveExpressions.connect(self.handleSaveExpressions)

    def handleExpressionLoaded(self, data):
        self.labelList = data[0]
        self.exprList = data[1]

        self.currentLineId = 0
        self.inputWidgets = []
        self.labelWidgets = []

        if self.inputListLayout is not None:
            while self.inputListLayout.count():
                item = self.inputListLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        for i in range(len(self.labelList)):
            btn = self.createLabelButton(self.labelList[i], self.currentLineId)
            box = self.createInputBox(self.exprList[i], self.currentLineId)
            self.inputListLayout.addWidget(btn, i, 0)
            self.inputListLayout.addWidget(box, i, 1)
            self.labelWidgets.append(btn)
            self.inputWidgets.append(box)
            self.currentLineId += 1

        print(self.labelList)

    def handleSaveExpressions(self):
        launchWriter(self.labelList, self.exprList)

    def changeExpr(self, line_id: int, expr: str):
        self.inputWidgets[line_id].setText(expr)
        self.exprList[line_id] = expr

    def changeActiveLineId(self, line_id: int):
        self.currentExprNum = line_id
        self.inputListLayout.count()
        for i in range(self.inputListLayout.count()):
            w = self.inputListLayout.itemAt(i).widget()
            if isinstance(w, CustomLabel):
                if w.line_id == line_id:
                    w.setActive(True)
                else:
                    w.setActive(False)

    def handleGraphComplete(self, consoleData: ConsoleData):
        # ~ print("in console")
        # ~ print(consoleData.truthTable)

        # evil code

        self.changeExpr(self.currentExprNum, consoleData.expression)

        # save code
        self.truthTable.setColumnCount(len(consoleData.truthTable))
        self.truthTable.setRowCount(len(consoleData.truthTable[0]))
        # ~ layout.addWidget(button2)

        for i in range(len(consoleData.truthTable)):
            for j in range(len(consoleData.truthTable[0])):
                # ~ print (consoleData.truthTable[i][j])
                item = QTableWidgetItem()
                item.setText(str(consoleData.truthTable[i][j]))
                # ~ tmplayout.addWidget(item)
                self.truthTable.setItem(j, i, item)

    def drawGraph(self, expr: str, label: str):
        self.DrawGraphCommand.emit([expr, label])

    def addRecord(self, label, expr=None):
        self.currentLineId += 1
        if expr is None:
            expr = self.exprList[-1]
        newBtn = self.createLabelButton(label, self.currentLineId)
        newBox = self.createInputBox(expr, self.currentLineId)
        self.inputListLayout.addWidget(newBtn, self.currentLineId + 1, 0)
        self.inputListLayout.addWidget(newBox, self.currentLineId + 1, 1)
        self.labelWidgets.append(newBtn)
        self.inputWidgets.append(newBox)
        self.inputListWidget.setMinimumHeight(40 * len(self.inputWidgets))

    def newInputBoxEvent(self):
        # ~ self.currentExprNum += 1
        label = chr(ord(self.labelList[-1]) + 1)
        self.labelList.append(label)
        self.exprList.append("A & B")
        self.addRecord(label)

    def createLabelButton(self, label, line_id):
        newButton = CustomLabel(label, line_id)
        newButton.setFlat(True)
        newButton.setMinimumWidth(40)
        newButton.setMinimumHeight(40)
        newButton.setMaximumWidth(40)
        newButton.setMaximumHeight(40)
        return newButton

    def createInputBox(self, content: str, inputId: int):
        currentLineEdit = CustomEditWidget(content, inputId)
        currentLineEdit.setMinimumWidth(240)
        currentLineEdit.setMinimumHeight(38)
        currentLineEdit.setTextMargins(2, 4, 4, 2)
        currentLineEdit.inputChangeEvent.connect(self.selectInputBoxChange)
        currentLineEdit.inputEditedEvent.connect(self.selectInputBoxEdited)
        return currentLineEdit

    def selectInputBoxChange(self, lineId):
        print("LINE ID: ", lineId)
        widget: CustomEditWidget = self.inputWidgets[lineId]
        self.exprList[lineId] = widget.text()
        self.drawGraph(self.exprList[lineId], self.labelList[lineId])
        self.changeActiveLineId(lineId)

    def selectInputBoxEdited(self, lineId):
        print("LINE ID: ", lineId)
        self.inputListWidget.setMinimumWidth(420)
        widget: CustomEditWidget = self.inputWidgets[lineId]
        if len(widget.text()) > 20:
            print(len(widget.text()), self.lineEditWidth)
            # ~ self.inputWidgets[lineId].setMaximumWidth(self.lineEditWidth+20)
            self.lineEditWidth = self.lineEditWidth + 4
            self.inputWidgets[lineId].setMinimumWidth(self.lineEditWidth)
        self.changeActiveLineId(lineId)

    def createNewButton(self):
        newButton = QPushButton('+')
        newButton.resize(40, 40)
        newButton.clicked.connect(self.newInputBoxEvent)
        return newButton

    def newCNFExpr(self):
        newExpr = self.exprList[self.currentExprNum]
        newExpr = cnf(newExpr)
        self.exprList.append(newExpr)
        self.labelList.append("CNF")
        self.addRecord("CNF", newExpr)

    def newDNFExpr(self):
        newExpr = self.exprList[self.currentExprNum]
        newExpr = dnf(newExpr)
        self.exprList.append(newExpr)
        self.labelList.append("DNF")
        self.addRecord("DNF", newExpr)

    def newSIMExpr(self):
        newExpr = self.exprList[self.currentExprNum]
        newExpr = simplify(newExpr)
        self.exprList.append(newExpr)
        self.labelList.append("SIM")
        self.addRecord("SIM", newExpr)
