from PySide6.QtWidgets import QFrame, QWidget


class GraphWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white")