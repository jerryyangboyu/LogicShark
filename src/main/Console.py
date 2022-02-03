from PySide6.QtWidgets import QFrame, QWidget, QToolButton

from PySide6.QtGui import QIcon


class ConsoleWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.setMaximumHeight(300)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #00CCFF")




