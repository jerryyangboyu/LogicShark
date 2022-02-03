from PySide6.QtWidgets import QFrame, QWidget


class ComponentWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.setMinimumSize(200, 400)
        self.setMaximumWidth(400)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #00CCFF")
