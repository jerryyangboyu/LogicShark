import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QGridLayout, QMenu, QApplication

import Component
import Console
import Graph
import ToolBar
from src.LogicTypes import ConsoleData


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
        # self.AppWidget.setStyleSheet("background-color: white")

        # Set the default central widgets for main layout, others might be docking components
        self.setCentralWidget(self.AppWidget)

        self.createMenu()

        self.ToolbarWidget.ClearScreenCommand.connect(self.clearScreenCommand)
        self.GraphWidget.OnGraphFinished.connect(self.handleGraphFinished)
        self.ConsoleWidget.DrawGraphCommand.connect(self.drawGraphCommand)
        self.ToolbarWidget.SaveImageCommand.connect(self.exportGraph)
        self.ToolbarWidget.LoadExpressions.connect(self.handleLoadExpressions)
        self.ToolbarWidget.SaveExpressions.connect(self.handleSaveExpressions)

        # test
        self.ConsoleWidget.handleExpressionLoaded([["A"], ["B"]])

    def handleSaveExpressions(self):
        self.ConsoleWidget.SaveExpressions.emit()

    def handleLoadExpressions(self, data):
        self.ConsoleWidget.ExpressionLoaded.emit(data)

    def createMenu(self):
        self.Menu: QMenu = self.menuBar().addMenu("&About")
        self.AboutAction = QAction("Info")
        self.TurorialAction = QAction("Tutorial")
        self.Menu.addAction(self.AboutAction)
        self.Menu.addAction(self.TurorialAction)

    def clearScreenCommand(self):
        self.GraphWidget.ClearScreenSignal.emit()

    def handleGraphFinished(self, consoleData: ConsoleData):
        self.ConsoleWidget.OnGraphFinished.emit(consoleData)

    def drawGraphCommand(self, command):
        print(command)
        self.GraphWidget.DrawGraphSignal.emit(command)

    def exportGraph(self, loc: str):
        self.GraphWidget.ExportCommand.emit(loc)


app = QApplication(sys.argv)

# QDir.addSearchPath("icons", QDir("./resources").absolutePath())
# print(QDir("./resources").absolutePath())

main_widget = MainWindow()

main_widget.setWindowTitle("Logic Shark")
main_widget.show()

sys.exit(app.exec())
