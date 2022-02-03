from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QToolButton, QLabel


class ToolBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white")

        self.logoWidget = QLabel()
        pixelMap = QPixmap("icons:logo.jpg")
        self.logoWidget.setPixmap(pixelMap)

