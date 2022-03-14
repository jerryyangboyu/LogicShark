from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class TitleFrame(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)

        self.TitleWidget = QLabel()
        self.TitleWidget.setText(title)

        self.TitleWidget.setFont("Arial")
        self.TitleWidget.setStyleSheet("""
            padding: 10;
            border: 1px solid black;
            color: black;
            font-weight: bold;
            border-radius: 10;
            background-color: #ffff94
        """)
        self.TitleWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TitleWidget.setFixedWidth(100)
        self.TitleWidget.setMaximumHeight(40)

        self.WidgetLayout = QVBoxLayout()
        self.WidgetLayout.addWidget(self.TitleWidget)

        self.setLayout(self.WidgetLayout)

    def addChildWidget(self, childWidget: QWidget):
        self.WidgetLayout.addWidget(childWidget)

