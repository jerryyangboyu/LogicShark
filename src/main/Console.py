from PySide6.QtWidgets import QFrame, QWidget, QToolButton

from PySide6.QtGui import QIcon


class ConsoleWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        self.setMinimumWidth(200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #00CCFF")




