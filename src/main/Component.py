from PySide6.QtWidgets import QFrame, QWidget


class ComponentWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 300)
        self.setMaximumWidth(300)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #00CCFF")
