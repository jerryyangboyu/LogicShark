from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QDockWidget
from PySide6.QtCore import Qt
from src.main import Graph, Console, Component


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dockWidget = None
        self.logoWidget = None
        self.logoBar = None

        # self.createToolBar()

        horizontal_layout = QHBoxLayout()
        vertical_layout = QVBoxLayout(horizontal_layout.widget())
        vertical_layout.addWidget(Graph.GraphWidget(horizontal_layout.widget()))
        vertical_layout.addWidget(Console.ConsoleWidget(horizontal_layout.widget()))

        horizontal_layout.addWidget(Component.ComponentWidget(self))
        horizontal_layout.addLayout(vertical_layout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(horizontal_layout)
        self.setCentralWidget(self.mainWidget)


    def createToolBar(self):
        self.logoWidget = QLabel()
        pixelMap = QPixmap("icons:logo.jpg")
        self.logoWidget.setPixmap(pixelMap)

        self.dockWidget = QDockWidget()
        self.dockWidget.setWidget(self.logoWidget)


        # self.toolbar = self.addToolBar("logo")

        # self.toolbar.addWidget(self.logoWidget)

        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.dockWidget)



        # QLabel * l = new
        # QLabel(this);
        # l->setPixmap(QPixmap(":/myresource.png"));
        # toolBar->addWidget(l);

        # self.logoBar.addWidget(self.logoWidget)


