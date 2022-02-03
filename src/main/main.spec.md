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