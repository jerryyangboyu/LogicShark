from PySide6.QtCore import QSize, QRect, Signal
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QToolButton, QLabel, QPushButton, \
    QSizePolicy, QGroupBox, QFileDialog

from algorithm import cnf, dnf, simplify
from fileHandling import launchReader, launchWriter, readAllFileWithExtension


class ToolBar(QFrame):
    ClearScreenCommand = Signal()
    SaveImageCommand = Signal(str)
    LoadExpressions = Signal(list)
    SaveExpressions = Signal()
    CNF = Signal()
    DNF = Signal()
    SIM = Signal()

    def __init__(self):
        super().__init__()

        # Set Styles
        self.setFixedHeight(80)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white")

        # Declare Components
        self.LogoWidget = self.createLogoWidget()
        self.GraphButtonGroup = self.createGraphButtonGroup()
        self.FunctionButtonGroup = self.createFunctionButtonGroup()

        # Create Layout
        self.ToolbarLayout = QHBoxLayout()
        self.ToolbarLayout.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.ToolbarLayout.addWidget(self.LogoWidget)
        self.ToolbarLayout.addWidget(self.GraphButtonGroup)
        self.ToolbarLayout.addWidget(self.FunctionButtonGroup)
        self.setLayout(self.ToolbarLayout)

    def createGraphButtonGroup(self):
        GroupBox = QGroupBox()
        GroupBox.setTitle("Graph")
        GroupBoxLayout = QHBoxLayout()
        # button1 = QPushButton('NEW')
        button2 = QPushButton('OPEN')
        button3 = QPushButton('SAVE')
        button4 = QPushButton('EXPORT')
        # GroupBoxLayout.addWidget(button1)
        GroupBoxLayout.addWidget(button2)
        GroupBoxLayout.addWidget(button3)
        GroupBoxLayout.addWidget(button4)
        GroupBox.setLayout(GroupBoxLayout)

        # Button signal handling
        # button1.clicked.connect(self.clickedNewButton)
        button2.clicked.connect(self.clickedOpenButton)
        button3.clicked.connect(self.clickedSaveButton)
        button4.clicked.connect(self.clickedExportButton)
        return GroupBox

    def createFunctionButtonGroup(self):
        GroupBox = QGroupBox()
        GroupBox.setTitle("Functions")
        GroupBoxLayout = QHBoxLayout()
        button5 = QPushButton("CNF")
        button6 = QPushButton("DNF")
        button7 = QPushButton("Simplify")
        # button8 = QPushButton("Custom")
        button9 = QPushButton("Clear")
        GroupBoxLayout.addWidget(button5)
        GroupBoxLayout.addWidget(button6)
        GroupBoxLayout.addWidget(button7)
        # GroupBoxLayout.addWidget(button8)G
        GroupBoxLayout.addWidget(button9)
        GroupBox.setLayout(GroupBoxLayout)

        # Button signal handling
        button5.clicked.connect(self.clickedCNFButton)
        button6.clicked.connect(self.clickedDNFButton)
        button7.clicked.connect(self.clickedSimplifyButton)
        # button8.clicked.connect(self.clickedCustomButton)
        button9.clicked.connect(self.clickedClearButton)
        return GroupBox

    def clickedNewButton(self):
        print("NEW")

    def clickedOpenButton(self):
        labels, exprs = launchReader()
        self.LoadExpressions.emit([labels, exprs])
        print("R:", exprs)
        print("OPEN")

    def clickedSaveButton(self):
        self.SaveExpressions.emit()
        print("SAVE")

    def clickedExportButton(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', 'default.png', "Image file (*.png)")
        self.SaveImageCommand.emit(fileName)

    def clickedCNFButton(self):
        self.CNF.emit()

    def clickedDNFButton(self):
        self.DNF.emit()

    def clickedSimplifyButton(self):
        self.SIM.emit()

    def clickedCustomButton(self):
        print("CUSTOM")

    def clickedClearButton(self):
        self.ClearScreenCommand.emit()

    def createLogoWidget(self):
        logoWidget = QLabel()
        pixelMap = QPixmap("src/resources/logo.jpg")

        w = min(pixelMap.width(), self.maximumWidth())
        h = min(pixelMap.height(), self.maximumHeight() - 20)
        pixelMap = pixelMap.scaled(QSize(w, h), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logoWidget.setPixmap(pixelMap)
        return logoWidget
