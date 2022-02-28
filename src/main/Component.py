from PySide6.QtCore import QObject, Qt, QPoint, QMimeData
from PySide6.QtGui import Qt, QPainter, QColor, QDrag
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from TitleFrame import TitleFrame

from src.main.DiagramItem import ANDLogicGateItem, SourceLogicGateItem


class ComponentCore(QWidget, QObject):
    def __init__(self):
        super().__init__()
        self.GridLayout = QGridLayout()

        self.AndGateLabel = ANDLogicGateItem().getLabelWidget()
        self.OrGateLabel = ANDLogicGateItem().getLabelWidget()
        self.NotGateLabel = ANDLogicGateItem().getLabelWidget()
        self.IN1 = SourceLogicGateItem("X", True).getLabelWidget()
        self.OUT1 = SourceLogicGateItem("Y", False).getLabelWidget()

        self.GridLayout.addWidget(self.AndGateLabel, 0, 0)
        self.GridLayout.addWidget(self.OrGateLabel, 0, 1)
        self.GridLayout.addWidget(self.NotGateLabel, 1, 0)
        self.GridLayout.addWidget(self.IN1, 1, 1)
        self.GridLayout.addWidget(self.OUT1, 2, 0)
        self.GridLayout.setRowStretch(3, 10)
        self.GridLayout.setColumnStretch(2, 10)

        self.setLayout(self.GridLayout)

    def mousePressEvent(self, event):
        child: QLabel = self.childAt(event.position().toPoint())
        if not child:
            return

        pixmap = child.pixmap()
        label_type = child.accessibleName()
        location = QPoint(event.position().toPoint() - child.pos())
        data = [label_type, str(location.x()), str(location.y())]

        mime_data = QMimeData()
        # TODO This is not the most elegant solution so far
        mime_data.setData("application/logicgate-graph-data", bytes("|".join(data), "utf-8"))

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)  # 保证拖拽的时候有图片在显示
        drag.setHotSpot(event.position().toPoint() - child.pos())

        # 在拖拽的时候给原来的图片加上阴影
        temp_pixmap = pixmap.copy()
        painter = QPainter()
        painter.begin(temp_pixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        child.setPixmap(temp_pixmap)

        if drag.exec(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/logicgate-graph-data"):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


class ComponentWidget(TitleFrame, QObject):
    def __init__(self):
        super().__init__("TOOL")

        self.setMinimumSize(320, 280)
        self.setMaximumWidth(280)
        self.setStyleSheet("background-color: #00ccff")

        self.CoreComponent = ComponentCore()
        # self.CoreComponent.setObjectName("CoreComponent")
        # self.CoreComponent.setStyleSheet("""
        #                     QWidget#CoreComponent {
        #                         background-color: yellow
        #                     }""")
        self.addChildWidget(self.CoreComponent)
