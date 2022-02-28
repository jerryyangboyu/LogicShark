from PySide6.QtWidgets import QFrame, QWidget, QToolButton
from TitleFrame import TitleFrame
from PySide6.QtGui import QIcon


class Console(QWidget):
    def __init__(self):
        super().__init__()


class ConsoleWidget(TitleFrame):
    def __init__(self):
        super().__init__("CONSOLE")
        self.setFixedHeight(200)
        self.setMinimumWidth(200)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #00CCFF")

        self.Console = Console()
        self.addChildWidget(self.Console)
