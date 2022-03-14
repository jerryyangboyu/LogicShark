import sys

import PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QGridLayout, QMenu, QApplication
import ToolBar, Component, Graph, Console


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Register main widgets in run time
        self.GraphWidget = Graph.GraphWidget()
        self.ConsoleWidget = Console.ConsoleWidget()
        self.ComponentWidget = Component.ComponentWidget()
        self.ToolbarWidget = ToolBar.ToolBar()

        # Register Menu and Actions
        self.Menu = None

        # Set layout for main part: components, graph and console
        # Our first attempt is the fix the position of each UI components
        self.CoreUILayout = QGridLayout()
        self.CoreUILayout.addWidget(self.ComponentWidget, 0, 0, 2, 1)  # row=0, column=0, rowSpan=3, columnSpan=1
        self.CoreUILayout.addWidget(self.GraphWidget, 0, 1)  # row=0, column=1
        self.CoreUILayout.addWidget(self.ConsoleWidget, 1, 1)  # row=1, column=1
        self.CoreUILayout.setSpacing(10)

        # Set the app layout including CoreUI and toolbar
        self.AppLayout = QVBoxLayout()
        self.AppLayout.addWidget(self.ToolbarWidget)
        self.AppLayout.addLayout(self.CoreUILayout)
        self.AppLayout.setSpacing(10)

        # Create Main Widgets from Main Layout
        self.AppWidget = QWidget()
        self.AppWidget.setLayout(self.AppLayout)
        self.AppWidget.setStyleSheet("background-color: white")

        # Set the default central widgets for main layout, others might be docking components
        self.setCentralWidget(self.AppWidget)

        self.createMenu()

    def createMenu(self):
        self.Menu: QMenu = self.menuBar().addMenu("&About")
        self.AboutAction = QAction("Info")
        self.TurorialAction = QAction("Tutorial")
        self.Menu.addAction(self.AboutAction)
        self.Menu.addAction(self.TurorialAction)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    PySide6.QtCore.QDir.addSearchPath("icons", "resources")

    main_widget = MainWindow()

    main_widget.setWindowTitle("Logic Shark")
    main_widget.show()

    sys.exit(app.exec())
