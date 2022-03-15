from PySide6.QtCore import QSize, QRect, Signal, QDir
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QToolButton, QLabel, QPushButton, \
    QSizePolicy, QGroupBox
from Graph import GraphScene


class ToolBar(QFrame):

    ClearScreenCommand = Signal()

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
        self.FunctionButtonGroup = self.createFunctionButtonGroup()

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
        GroupBoxLayout.addWidget(QPushButton("NEW"))
        GroupBoxLayout.addWidget(QPushButton("OPEN"))
        GroupBoxLayout.addWidget(QPushButton("SAVE"))
        GroupBoxLayout.addWidget(QPushButton("EXPORT"))
        GroupBox.setLayout(GroupBoxLayout)
        return GroupBox

    def createFunctionButtonGroup(self):
        GroupBox = QGroupBox()
        GroupBox.setTitle("Functions")
        GroupBoxLayout = QHBoxLayout()
        GroupBoxLayout.addWidget(QPushButton("CNF"))
        GroupBoxLayout.addWidget(QPushButton("DNF"))
        GroupBoxLayout.addWidget(QPushButton("Simplify"))
        GroupBoxLayout.addWidget(QPushButton("Custom"))
        GroupBoxLayout.addWidget(self.createClearButton())
        GroupBox.setLayout(GroupBoxLayout)
        return GroupBox

    def createClearButton(self):
        btn = QPushButton("Clear")
        btn.clicked.connect(self.handleClear)
        return btn

    def handleClear(self):
        print("btn clicked")
        self.ClearScreenCommand.emit()

    def createLogoWidget(self):
        logoWidget = QLabel()

        pixelMap = QPixmap("src/resources/logo.jpg")

        w = min(pixelMap.width(), self.maximumWidth())
        h = min(pixelMap.height(), self.maximumHeight() - 20)
        pixelMap = pixelMap.scaled(QSize(w, h), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logoWidget.setPixmap(pixelMap)
        return logoWidget

