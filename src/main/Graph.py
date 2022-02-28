from typing import Type

import PySide6
from PySide6.QtCore import Qt, QByteArray, QDataStream, QPoint, QIODevice, QPointF, QLineF
from PySide6.QtGui import QPixmap, QTransform, QPainterPath, QPen, QColor
from PySide6.QtWidgets import QFrame, QWidget, QGraphicsScene, QGraphicsView, QLabel, QGraphicsLineItem, \
    QGraphicsPathItem, QGraphicsSceneMouseEvent
from TitleFrame import TitleFrame
from src.main.Component import ComponentCore
from src.main.DiagramItem import LogicGateItem, ANDLogicGateItem, LineItem, NodeType, SourceLogicGateItem

from enum import Enum
from src.main.DiagramItem import LogicGateType


class GraphicState(Enum):
    MouseMove, InsertLine, InsertItem = range(3)


class GraphScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # InsertLine states
        self.pathItem = None
        self.startPos = None
        self.currentLean: NodeType = None

        # General states
        self.state = GraphicState.MouseMove

    def dragEnterEvent(self, event: PySide6.QtWidgets.QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/logicgate-graph-data"):
            if event.source() == self or event.source() is ComponentCore:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/logicgate-graph-data"):
            if event.source() == self or event.source() is ComponentCore:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: PySide6.QtWidgets.QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/logicgate-graph-data"):
            byte_data: QByteArray = event.mimeData().data("application/logicgate-graph-data")
            list_data = byte_data.data().decode("utf-8").split("|")
            offset = QPoint(int(list_data[1]), int(list_data[2]))
            label_type = list_data[0]
            if label_type == LogicGateType.AND.name:
                graphic_item = ANDLogicGateItem()
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
            elif label_type == LogicGateType.INPUT_NODE.name:
                # TODO
                # assign next Name here, from A, B, C, D ...
                graphic_item = SourceLogicGateItem("X", True)
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
            elif label_type == LogicGateType.OUTPUT_NODE.name:
                graphic_item = SourceLogicGateItem("Y", False)
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        gate = self.itemAt(event.scenePos(), QTransform())
        # start connecting line
        if gate is not None and type(gate) is ANDLogicGateItem:
            lean = gate.atConnectionPoint(event.scenePos())
            if lean != NodeType.NoneNode:
                self.startPos = gate.getNodeScenePos(lean)
                self.currentLean = lean
                self.pathItem = QGraphicsPathItem()
                self.pathItem.setPen(QPen(QColor("red"), 5))
                path = QPainterPath()
                path.moveTo(self.startPos)
                path.lineTo(self.startPos)
                self.pathItem.setPath(path)
                self.addItem(self.pathItem)
                self.state = GraphicState.InsertLine

        super(GraphScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        # Continue line insertion
        if self.state == GraphicState.InsertLine and self.pathItem is not None:
            # if left leaning, if left add is allowed, vice versa for right leaning
            if (self.currentLean.isInputNode() and event.scenePos().x() <= self.startPos.x()) \
                    or (self.currentLean.isOutputNode() and event.scenePos().x() >= self.startPos.x()):
                path = LineItem.getZigZagLine(self.startPos, event.scenePos())
                self.pathItem.setPath(path)

        elif self.state == GraphicState.MouseMove:
            super(GraphScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.state == GraphicState.InsertLine and self.pathItem is not None:
            endNode = self.itemAt(event.scenePos(), QTransform())

            # if node is LogicGate & valid connect node then create new line
            if endNode is not None:
                print(endNode, type(endNode) is SourceLogicGateItem)

                if type(endNode) == ANDLogicGateItem:
                    nodeType = endNode.atConnectionPoint(event.scenePos())
                    if nodeType is not NodeType.NoneNode \
                            and LineItem.isValidConnection(self.currentLean, nodeType):
                        startNode = self.itemAt(self.startPos, QTransform())
                        newLineItem = LineItem(startNode, self.currentLean, endNode, nodeType)
                        self.addItem(newLineItem)
                elif type(endNode) is SourceLogicGateItem:
                    # TODO 这里有个bug就是有时候会连不上子node，但是属于corner cases，请日后完善测试注意输出 @Qiren Dong
                    print("inputCheck", endNode.isInputNode and self.currentLean.isInputNode())
                    print("outputCheck", not endNode.isInputNode and self.currentLean.isOutputNode())
                    if (endNode.isInputNode and self.currentLean.isInputNode()) \
                            or (not endNode.isInputNode and self.currentLean.isOutputNode()):
                        print("constructing line")
                        startNode = self.itemAt(self.startPos, QTransform())
                        newLineItem = LineItem(startNode, self.currentLean, endNode, NodeType.SourceNode)
                        self.addItem(newLineItem)

            # remove old temp line
            self.removeItem(self.pathItem)
            self.pathItem = None
            self.startPos = None
            self.currentLean = None
            self.state = GraphicState.MouseMove
        super(GraphScene, self).mouseReleaseEvent(event)


class GraphWidget(TitleFrame):
    def __init__(self):
        super().__init__("GRAPH")
        self.setMinimumSize(200, 400)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white")

        self.GraphScene = GraphScene()
        self.GraphicView = QGraphicsView(self.GraphScene)
        self.addChildWidget(self.GraphicView)
