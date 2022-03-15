from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QToolButton, QLabel, QPushButton, \
    QSizePolicy, QGroupBox

from algorithm import cnf, dnf, simplify


class ToolBar(QFrame):
    def __init__(self):
        super().__init__()

        # Set Styles
        self.setFixedHeight(80)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white; color: black")

        # Declare Components
        self.LogoWidget = self.createLogoWidget()
        self.GraphButtonGroup = ToolBar.createGraphButtonGroup()
        self.FunctionButtonGroup = ToolBar.createFunctionButtonGroup()

        # Create Layout
        self.ToolbarLayout = QHBoxLayout()
        self.ToolbarLayout.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.ToolbarLayout.addWidget(self.LogoWidget)
        self.ToolbarLayout.addWidget(self.GraphButtonGroup)
        self.ToolbarLayout.addWidget(self.FunctionButtonGroup)
        self.setLayout(self.ToolbarLayout)


    @staticmethod
    def createGraphButtonGroup():
        GroupBox = QGroupBox()
        GroupBox.setTitle("Graph")
        GroupBoxLayout = QHBoxLayout()
        button1 = QPushButton('NEW')
        button2 = QPushButton('OPEN')
        button3 = QPushButton('SAVE')
        button4 = QPushButton('EXPORT')
        GroupBoxLayout.addWidget(button1)
        GroupBoxLayout.addWidget(button2)
        GroupBoxLayout.addWidget(button3)
        GroupBoxLayout.addWidget(button4)
        GroupBox.setLayout(GroupBoxLayout)

        # Button signal handling
        button1.clicked.connect(ToolBar.clickedNewButton)
        button2.clicked.connect(ToolBar.clickedOpenButton)
        button3.clicked.connect(ToolBar.clickedSaveButton)
        button4.clicked.connect(ToolBar.clickedExportButton)
        return GroupBox


    @staticmethod
    def createFunctionButtonGroup():
        GroupBox = QGroupBox()
        GroupBox.setTitle("Functions")
        GroupBoxLayout = QHBoxLayout()
        button5 = QPushButton("CNF")
        button6 = QPushButton("DNF")
        button7 = QPushButton("Simplify")
        button8 = QPushButton("Custom")
        button9 = QPushButton("Clear")
        GroupBoxLayout.addWidget(button5)
        GroupBoxLayout.addWidget(button6)
        GroupBoxLayout.addWidget(button7)
        GroupBoxLayout.addWidget(button8)
        GroupBoxLayout.addWidget(button9)
        GroupBox.setLayout(GroupBoxLayout)

        # Button signal handling
        button5.clicked.connect(ToolBar.clickedCNFButton)
        button6.clicked.connect(ToolBar.clickedDNFButton)
        button7.clicked.connect(ToolBar.clickedSimplifyButton)
        button8.clicked.connect(ToolBar.clickedCustomButton)
        button9.clicked.connect(ToolBar.clickedClearButton)
        return GroupBox


    def clickedNewButton(self):
        print("NEW")

    def clickedOpenButton(self):
        print("OPEN")

    def clickedSaveButton(self):
        print("SAVE")

    def clickedExportButton(self):
        print("EXPORT")

    def clickedCNFButton(self):
        print('CNF: ')

    def clickedDNFButton(self):
        print('DNF: ')

    def clickedSimplifyButton(self):
        print('Simplify: ')

    def clickedCustomButton(self):
        print("CUSTOM")

    def clickedClearButton(self):
        print('CLEAR')

    def createLogoWidget(self):
        logoWidget = QLabel()
        pixelMap = QPixmap("icons:logo.jpg")

        w = min(pixelMap.width(), self.maximumWidth())
        h = min(pixelMap.height(), self.maximumHeight() - 20)
        pixelMap = pixelMap.scaled(QSize(w, h), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logoWidget.setPixmap(pixelMap)
        return logoWidget



