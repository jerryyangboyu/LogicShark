from typing import List

import PySide6
from PySide6.QtCore import Qt, QByteArray, QPoint, Signal
from PySide6.QtGui import QTransform, QPainterPath, QPen, QColor
from PySide6.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QGraphicsSceneMouseEvent
from TitleFrame import TitleFrame
from Component import ComponentCore
from DiagramItem import LogicGateItem, ANDLogicGateItem, ORLogicGateItem, NOTLogicGateItem, LineItem, \
    SourceLogicGateItem

from enum import Enum
from ASTNode import genSymbol, ASTGraph
from LogicTypes import LogicGateType, NodeType
from src.algorithm import dnf, cnf, simplify


class GraphicState(Enum):
    MouseMove, InsertLine, InsertItem = range(3)


class GraphScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # InsertLine states
        self.pathItem = None
        self.startPos = None
        self.currentLean: NodeType = None

        # General states
        self.state = GraphicState.MouseMove
        self.ast = ASTGraph()

        alg = ANDLogicGateItem()
        # alg.setPos(0, 0)
        #
        org = ORLogicGateItem()
        # org.setPos(0, 100)
        #
        orgT = ORLogicGateItem()
        # orgT.setPos(150, 50)
        #
        T = SourceLogicGateItem("Y", isInputNode=False)
        # T.setPos(250, 50)

        S1 = SourceLogicGateItem("S1", isInputNode=True)
        S2 = SourceLogicGateItem("S2", isInputNode=True)
        S3 = SourceLogicGateItem("S3", isInputNode=True)

        self.ast.addNode(alg)
        self.ast.addNode(org)
        self.ast.addNode(orgT)
        self.ast.addNode(T)
        self.ast.addNode(S1)
        self.ast.addNode(S2)
        self.ast.addNode(S3)

        self.ast.addRelation(T, NodeType.LeftNode, orgT, NodeType.TopNode)
        self.ast.addRelation(orgT, NodeType.LeftNode, alg, NodeType.TopNode)
        self.ast.addRelation(orgT, NodeType.RightNode, org, NodeType.TopNode)
        self.ast.addRelation(alg, NodeType.LeftNode, S1, NodeType.TopNode)
        self.ast.addRelation(alg, NodeType.RightNode, S2, NodeType.TopNode)
        self.ast.addRelation(org, NodeType.LeftNode, S2, NodeType.TopNode)
        self.ast.addRelation(org, NodeType.RightNode, S3, NodeType.TopNode)

        self.drawGraph()

        exprs, labels = self.ast.toExpressions()
        print("Label is: ", labels[0])
        print("Expression is: ", exprs[0])
        print("The dnf form is: ", dnf(exprs[0]))
        print("The cnf form is: ", cnf(exprs[0]))
        print("It can simplify as: ", simplify(exprs[0]))

        # self.addItem(alg)
        # self.addItem(org)
        # self.addItem(orgT)
        # self.addItem(T)
        #
        # self.drawNewLine(T, NodeType.INSourceNode, orgT, NodeType.TopNode)
        # self.drawNewLine(orgT, NodeType.LeftNode, alg, NodeType.TopNode)
        # self.drawNewLine(orgT, NodeType.RightNode, org, NodeType.TopNode)

        # # TODO debug line 无法连接的bug
        # item1 = ORLogicGateItem()
        # item2 = ANDLogicGateItem()
        # line = LineItem(item1, NodeType.TopNode, item2, NodeType.LeftNode)
        #
        # self.addItem(item1)
        # self.addItem(item2)
        # self.addItem(line)

    def removeItem(self, item: PySide6.QtWidgets.QGraphicsItem) -> None:
        if isinstance(item, LineItem):
            self.ast.removeRelation(item.start_item, item.end_item)
        elif isinstance(item, LogicGateItem):
            self.ast.removeNode(item)
            self.ast.printRelationship()
        super(GraphScene, self).removeItem(item)

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
                self.ast.addNode(graphic_item)
            elif label_type == LogicGateType.INPUT_NODE.name:
                # TODO
                # assign next Name here, from A, B, C, D ...
                graphic_item = SourceLogicGateItem(genSymbol(), True)
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
                self.ast.addNode(graphic_item)
            elif label_type == LogicGateType.OUTPUT_NODE.name:
                graphic_item = SourceLogicGateItem(genSymbol(), False)
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
                self.ast.addNode(graphic_item)
            elif label_type == LogicGateType.OR.name:
                graphic_item = ORLogicGateItem()
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
                self.ast.addNode(graphic_item)
            elif label_type == LogicGateType.NOT.name:
                graphic_item = NOTLogicGateItem()
                graphic_item.setPos(event.scenePos())
                self.addItem(graphic_item)
                self.ast.addNode(graphic_item)
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
        if gate is not None and isinstance(gate, LogicGateItem):
            lean = gate.atConnectionPoint(event.scenePos())
            if lean != NodeType.NoneNode:
                self.startPos = gate.getNodeScenePos(lean)
                self.currentLean = lean
                self.pathItem = QGraphicsPathItem()
                self.pathItem.setPen(QPen(QColor(Qt.black), 5))
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
            if isinstance(endNode, LogicGateItem):
                # TODO 这里有个bug就是有时候会连不上子node，但是属于corner cases，请日后完善测试注意输出 @Qiren Dong
                print("inputCheck", endNode, self.currentLean.isInputNode())
                print("outputCheck", endNode, self.currentLean.isOutputNode())
                nodeType = endNode.atConnectionPoint(event.scenePos())
                if nodeType is not NodeType.NoneNode \
                        and LineItem.isValidConnection(self.currentLean, nodeType):
                    startNode = self.itemAt(self.startPos, QTransform())
                    if isinstance(startNode, LogicGateItem):
                        self.drawNewLine(startNode, self.currentLean, endNode, nodeType)
                        self.connectLogicLine(startNode, self.currentLean, endNode, nodeType)

            # remove old temp line
            self.removeItem(self.pathItem)
            self.pathItem = None
            self.startPos = None
            self.currentLean = None
            self.state = GraphicState.MouseMove
        super(GraphScene, self).mouseReleaseEvent(event)

    def connectLogicLine(self, s, l1, e, l2):
        # self.ast.addRelation(s, l1, e, l2)
        exprs = self.ast.toExpressions()
        if len(exprs) != 0:
            self.parent.postGraphFinished(exprs)
        print(self.parent, exprs)

    def drawNewLine(self, s, l1, e, l2):
        newLineItem = LineItem(s, l1, e, l2)
        self.addItem(newLineItem)
        newLineItem.show()
        print("is new item in the scene: ", newLineItem in self.items())

    def drawGraph(self, expr: str = None):
        self.clear()
        # self.ast = ASTGraph.fromExpression(expr)
        root = self.ast.findRoot().pop()

        width_interval = 100
        height_interval = 150
        current_height = 0

        rootItem = SourceLogicGateItem(root.label, isInputNode=False)
        rootItem.setPos(0, 0)
        rootItem.setId(root.node_id)
        self.addItem(rootItem)

        firstOp = self.ast.adjList[root.leftChild]
        firstOp.parent.append(rootItem)
        firstOp.leans.append(NodeType.LeftNode)

        q = [firstOp]
        distToSource = [-1] * len(self.ast.adjList)
        distToSource[firstOp.node_id] = 1

        count = 0
        while len(q) != 0:
            count += 1
            v = q.pop(0)

            if current_height + 1 == distToSource[v.node_id]:
                current_height += 1

            posX = -height_interval * current_height
            expected_width = 2 ** (current_height - 1)
            offset = count - 2 ** (current_height - 1)
            mid = (expected_width - 1) / 2
            posY = (offset - mid) * width_interval

            item = None
            if v.symbol_type == LogicGateType.AND:
                item = ANDLogicGateItem()
            elif v.symbol_type == LogicGateType.NOT:
                item = NOTLogicGateItem()
            elif v.symbol_type == LogicGateType.OR:
                item = ORLogicGateItem()
            elif v.symbol_type == LogicGateType.INPUT_NODE:
                item = SourceLogicGateItem(v.label, isInputNode=True)

            item.setPos(posX, posY)
            item.setId(v.node_id)
            self.addItem(item)
            for i in range(len(v.parent)):
                self.drawNewLine(item, NodeType.TopNode, v.parent[i], v.leans[i])

            if v.leftChild != -1:
                w = v.leftChild
                l = self.ast.adjList[w]
                l.parent.append(item)
                l.leans.append(NodeType.LeftNode)
                if distToSource[w] == -1:
                    q.append(l)
                    distToSource[w] = distToSource[v.node_id] + 1

            if v.rightChild != -1:
                w = v.rightChild
                r = self.ast.adjList[w]
                r.parent.append(item)
                r.leans.append(NodeType.RightNode)
                if distToSource[w] == -1:
                    q.append(r)
                    distToSource[w] = distToSource[v.node_id] + 1


class GraphWidget(TitleFrame):
    ClearScreenSignal = Signal()
    DrawGraphSignal = Signal(str)
    OnGraphFinished = Signal(object)

    def __init__(self):
        super().__init__("GRAPH")
        self.setMinimumSize(200, 400)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white")

        self.GraphScene = GraphScene(self)
        self.GraphicView = QGraphicsView(self.GraphScene)
        self.addChildWidget(self.GraphicView)

        self.ClearScreenSignal.connect(self.handleClearScreen)
        self.DrawGraphSignal.connect(self.handleDrawSignal)

    def handleDrawSignal(self, expr: str):
        self.GraphScene.drawGraph(expr)

    def handleClearScreen(self):
        self.GraphScene.clear()

    def postGraphFinished(self, exprs: List[str]):
        self.OnGraphFinished.emit(exprs)
