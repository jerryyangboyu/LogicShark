可以使用dock来进行组件的布局

```python
# examples
self.logoWidget = QLabel()
pixelMap = QPixmap("icons:logo.jpg")
self.logoWidget.setPixmap(pixelMap)

self.dockWidget = QDockWidget()
self.dockWidget.setWidget(self.logoWidget)

self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.dockWidget)
```

How to create logo widget

```python
self.logoWidget = QLabel()
pixelMap = QPixmap("icons:logo.jpg")
self.logoWidget.setPixmap(pixelMap)
```

A Layout Method using Grid
```python
# self.createToolBar()

        # horizontal_layout = QHBoxLayout()
        # vertical_layout = QVBoxLayout(horizontal_layout.widget())
        # vertical_layout.addWidget(self.graphWidget)
        # vertical_layout.addWidget(self.consoleWidget)
        #
        # horizontal_layout.addWidget(Component.ComponentWidget(self))
        # horizontal_layout.addLayout(vertical_layout)
        #
        # toolbar_layout = QVBoxLayout()
        # toolbar_layout.addWidget(ToolBar.ToolBar())

        # self.setCentralWidget(self.mainWidget)
```

We use grid method for final layout, see
https://doc.qt.io/qtforpython/PySide6/QtWidgets/QGridLayout.html#PySide6.QtWidgets.PySide6.QtWidgets.QGridLayout.setColumnStretch

How we managed to resize the image of logo
https://stackoverflow.com/questions/10915215/pyqt-qt-how-to-stretch-an-image-in-qlabel-widget

We can use the addToolBar API to manage the floating toolbar, but it has constrains