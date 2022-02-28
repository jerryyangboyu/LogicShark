from enum import Enum
from typing import Optional

import PySide6
from PySide6.QtCore import QPointF, Qt, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPathStroker, QPainterPath, QPixmap, QPen
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QLabel, \
    QGraphicsTextItem

line_width = 3.6


class LogicGateType(Enum):
    AND, OR, NOT, INPUT_NODE, OUTPUT_NODE = range(5)


class NodeType(Enum):
    NoneNode, LeftNode, RightNode, TopNode, SourceNode = range(5)

    def isInputNode(self):
        return self.value == NodeType.LeftNode.value or self.value == NodeType.RightNode.value

    def isOutputNode(self):
        return self.value == NodeType.TopNode.value


class LogicGateItem(QGraphicsPathItem):
    width = 130
    height = 100
    symbolName = None

    def __init__(self, contextMenu=None, parent=None, scene=None):
        super().__init__(parent, scene)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def _draw(self, painter: QPainter):
        pass

    # This method use computed wireframe to render the image
    # Note that this method is independent from class, it is only used in Component Module
    # TODO IMPROVEMENT: use coordinate mapping function to increase resolution of image @Qiren Dong
    # more information see https://blog.csdn.net/fanyun_01/article/details/53129781
    def getLabelWidget(self) -> QLabel:
        label = QLabel()
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)  # Debug from 2022/2/26 4:30pm, you should assign a context to painter, aka activate
        self._draw(painter)
        painter.end()
        label.setPixmap(pixmap)
        label.setAccessibleName(self.symbolName)  # Use to distinguish what logic gate graph you are using
        label.setAttribute(Qt.WA_DeleteOnClose)  # Drag and Drop attribute
        return label

    def atConnectionPoint(self, cursorPos: QPointF) -> NodeType:
        return NodeType.NoneNode

    def getNodeScenePos(self, nodeType: NodeType = None) -> QPointF:
        return QPointF()


class ANDLogicGateItem(LogicGateItem):

    def __init__(self, contextMenu=None, parent=None, scene=None):
        super().__init__(parent, scene)
        self.symbolName = LogicGateType.AND.name
        self.setZValue(5)
        # All path coordinate, except essential one for drawing
        # Use QGraphicScene standard coordinate system
        self.main_path = None
        self.symbol_path = None
        self.symbol_path_stroke = None
        self.connect_path = None

        self.connect_point_left_path = None
        self.connect_point_left_stroke = None
        self.connect_point_right_path = None
        self.connect_point_right_stroke = None
        self.connect_point_top_path = None
        self.connect_point_top_stroke = None

        self.wireFrameOutlineWidth = 10

        self.leftPointRange = self._calculatePointRange(10, 35, 5)
        self.rightPointRange = self._calculatePointRange(10, 65, 5)
        self.topPointRange = self._calculatePointRange(120, 50, 5)

        self.setAcceptHoverEvents(True)  # For performance reason, this is auto closed

        self.defaultNodeColor = QColor(0, 255, 107)
        self.activeNodeColor = QColor(255, 107, 0)

        self.leftNodeColor = self.defaultNodeColor
        self.rightNodeColor = self.defaultNodeColor
        self.topNodeColor = self.defaultNodeColor

        self._createPath()
        self._createWireFrame()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: Optional[QWidget] = ...) -> None:
        painter.translate(-self.width / 2, -self.height / 2)
        self._draw(painter)

    def _draw(self, painter: QPainter):
        painter.fillPath(self.connect_path, QColor(Qt.black))

        painter.fillPath(self.symbol_path, QColor(255, 234, 0))
        painter.fillPath(self.symbol_path_stroke, QColor(Qt.black))

        painter.fillPath(self.connect_point_left_path, self.leftNodeColor)
        painter.fillPath(self.connect_point_left_stroke, QColor(Qt.black))

        painter.fillPath(self.connect_point_right_path, self.rightNodeColor)
        painter.fillPath(self.connect_point_right_stroke, QColor(Qt.black))

        painter.fillPath(self.connect_point_top_path, self.topNodeColor)
        painter.fillPath(self.connect_point_top_stroke, QColor(Qt.black))

    # This method calculate the shape of logic gate symbol
    # Note that it use (0, 0) coordinate as top-left corner AKA, it uses QPainter coordinate standard
    # However, self.main_path stick which QGraphicScene coordinate, so conversion is need when placed in graphic scene
    # Doc reference link:
    # - QPainter Class https://doc.qt.io/qt-5/qpainter.html#drawPath
    # - QPainterPath Class https://doc.qt.io/qt-5/qpainterpath.html#arcTo
    # Use PainterStroker, a tool to create outline of painting image,
    # see https://www.qtcentre.org/threads/43863-How-to-use-QPainterPathStroker
    # Last edit @Boyu Yang, 2022/2/26
    def _createPath(self):
        stroker = QPainterPathStroker()
        stroker.setCapStyle(Qt.RoundCap)
        stroker.setJoinStyle(Qt.RoundJoin)
        stroker.setWidth(0)

        connect_path = QPainterPath()
        connect_path.moveTo(10, 35 - line_width / 2)
        connect_path.lineTo(30, 35 - line_width / 2)
        connect_path.lineTo(30, 35 + line_width / 2)
        connect_path.lineTo(10, 35 + line_width / 2)

        connect_path.moveTo(10, 65 + line_width / 2)
        connect_path.lineTo(30, 65 + line_width / 2)
        connect_path.lineTo(30, 65 - line_width / 2)
        connect_path.lineTo(10, 65 - line_width / 2)

        connect_path.moveTo(95, 50 - line_width / 2)
        connect_path.lineTo(120, 50 - line_width / 2)
        connect_path.lineTo(120, 50 + line_width / 2)
        connect_path.lineTo(95, 50 + line_width / 2)
        connect_path.lineTo(95, 50 - line_width / 2)

        symbol_path = QPainterPath()
        # draw upper line
        symbol_path.moveTo(30, 20)
        symbol_path.lineTo(70, 20)
        # draw round
        bound_rect = QRectF(40, 20, 60, 60)
        symbol_path.arcTo(bound_rect, 90, -180)
        # draw lower line
        symbol_path.moveTo(70, 80)
        symbol_path.lineTo(30, 80)
        # close path
        symbol_path.lineTo(30, 20)
        symbol_path_stroke = stroker.createStroke(symbol_path)

        # draw connect points
        connect_point_left_path = QPainterPath()
        connect_point_left_path.addEllipse(QPointF(10, 35), 5, 5)
        connect_point_left_stroke = stroker.createStroke(connect_point_left_path)

        connect_point_right_path = QPainterPath()
        connect_point_right_path.addEllipse(QPointF(10, 65), 5, 5)
        connect_point_right_stroke = stroker.createStroke(connect_point_right_path)

        connect_point_top_path = QPainterPath()
        connect_point_top_path.addEllipse(QPointF(120, 50), 5, 5)
        connect_point_top_stroke = stroker.createStroke(connect_point_top_path)

        self.main_path = QPainterPath()
        self.main_path.addPath(symbol_path)
        self.main_path.addPath(symbol_path_stroke)
        self.main_path.addPath(connect_path)
        self.main_path.addPath(connect_point_left_path)
        self.main_path.addPath(connect_point_left_stroke)
        self.main_path.addPath(connect_point_right_path)
        self.main_path.addPath(connect_point_right_stroke)
        self.main_path.addPath(connect_point_top_path)
        self.main_path.addPath(connect_point_top_stroke)

        self.symbol_path = symbol_path
        self.symbol_path_stroke = symbol_path_stroke
        self.connect_path = connect_path
        self.connect_point_left_path = connect_point_left_path
        self.connect_point_left_stroke = connect_point_left_stroke
        self.connect_point_right_path = connect_point_right_path
        self.connect_point_right_stroke = connect_point_right_stroke
        self.connect_point_top_path = connect_point_top_path
        self.connect_point_top_stroke = connect_point_top_stroke

    def _createWireFrame(self):
        stroker = QPainterPathStroker()
        stroker.setCapStyle(Qt.RoundCap)
        stroker.setJoinStyle(Qt.RoundJoin)
        stroker.setWidth(self.wireFrameOutlineWidth)
        main_stroker = stroker.createStroke(self.main_path)
        self.main_path.addPath(main_stroker)
        self.main_path.translate(-self.width / 2, -self.height / 2)
        self.setPath(self.main_path)

    # This method find which node the cursor is current at, giving the pos of cursor
    # Input:
    # cursorPos: scenePos of cursor, type QPointF
    # Output:
    # 0 -> cursor on none of connecting point
    # 1 -> cursor on left input node
    # 2 -> cursor on right input node
    # 3 -> cursor on top output node
    def atConnectionPoint(self, cursorPos: QPointF) -> NodeType:
        relativePos = cursorPos - self.scenePos()
        if self.leftPointRange.contains(relativePos):
            return NodeType.LeftNode
        if self.rightPointRange.contains(relativePos):
            return NodeType.RightNode
        if self.topPointRange.contains(relativePos):
            return NodeType.TopNode
        return NodeType.NoneNode

    # Make input or output Node turn active color when user hover the mouse for the first time
    # TODO DEBUG: when mouse hover from right top side for left node, it do not turn active
    def hoverEnterEvent(self, event: PySide6.QtWidgets.QGraphicsSceneHoverEvent) -> None:
        lean = ANDLogicGateItem.atConnectionPoint(self, event.scenePos())
        print("hover enter with lean: ", lean)
        if lean == NodeType.LeftNode:
            self.leftNodeColor = self.activeNodeColor
        elif lean == NodeType.RightNode:
            self.rightNodeColor = self.activeNodeColor
        elif lean == NodeType.TopNode:
            self.topNodeColor = self.activeNodeColor
        super(ANDLogicGateItem, self).hoverEnterEvent(event)

    # Make input or output node turn to default state
    def hoverLeaveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.leftNodeColor = self.defaultNodeColor
        self.rightNodeColor = self.defaultNodeColor
        self.topNodeColor = self.defaultNodeColor
        super(ANDLogicGateItem, self).hoverLeaveEvent(event)

    # Input:
    # The central point use (0, 0) as top-left corner
    # cx: x-axis of central point
    # cy: y-axis of central point
    # radius: the radius of round shape
    def _calculatePointRange(self, cx, cy, radius) -> QRectF:
        rect = QRectF(cx - radius - self.wireFrameOutlineWidth / 2, cy - radius - self.wireFrameOutlineWidth / 2,
                      radius * 2 + self.wireFrameOutlineWidth, radius * 2 + self.wireFrameOutlineWidth)
        rect.translate(-self.width / 2, -self.height / 2)
        return rect

    # Get the scenePos of input or output node
    # Input:
    # 1 -> leftNode
    # 2 -> RightNode
    # 3 -> TopNode
    def getNodeScenePos(self, nodeType: NodeType) -> QPointF:
        if nodeType == NodeType.LeftNode:
            return self.mapToScene(10 - self.width / 2, 35 - self.height / 2)
        elif nodeType == NodeType.RightNode:
            return self.mapToScene(10 - self.width / 2, 65 - self.height / 2)
        elif nodeType == NodeType.TopNode:
            return self.mapToScene(120 - self.width / 2, 50 - self.height / 2)


class DiagramTextItem(QGraphicsTextItem):
    lost_focus = Signal(QGraphicsTextItem)

    def __init__(self, defaultText):
        super().__init__()
        self.setZValue(10)
        self.setPlainText(defaultText)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.lost_focus.emit(self)
        super(DiagramTextItem, self).focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
        super(DiagramTextItem, self).mouseDoubleClickEvent(event)


class SourceLogicGateItem(LogicGateItem):
    def __init__(self, defaultLabel: str, isInputNode=False):
        super().__init__()
        self.setZValue(5)
        self.isInputNode = isInputNode
        self.symbolName = LogicGateType.INPUT_NODE.name if isInputNode else LogicGateType.OUTPUT_NODE.name

        stroker = QPainterPathStroker()
        stroker.setCapStyle(Qt.RoundCap)
        stroker.setJoinStyle(Qt.RoundJoin)
        stroker.setWidth(0)

        if isInputNode:
            self.symbol_path = QPainterPath()
            self.symbol_path.addEllipse(QPointF(40, 50), 20, 20)
            self.symbol_path_stroke = stroker.createStroke(self.symbol_path)

            self.connect_path = QPainterPath()
            self.connect_path.moveTo(60, 50 - line_width / 2)
            self.connect_path.lineTo(80, 50 - line_width / 2)
            self.connect_path.lineTo(80, 50 + line_width / 2)
            self.connect_path.lineTo(60, 50 + line_width / 2)
            self.connect_path.lineTo(60, 50 - line_width / 2)

            self.connect_node_path = QPainterPath()
            self.connect_node_path.addEllipse(QPointF(80, 50), 5, 5)
            self.connect_node_stroke = stroker.createStroke(self.connect_node_path)
        else:
            self.symbol_path = QPainterPath()
            self.symbol_path.addEllipse(QPointF(90, 50), 20, 20)
            self.symbol_path_stroke = stroker.createStroke(self.symbol_path)

            self.connect_path = QPainterPath()
            self.connect_path.moveTo(70, 50 - line_width / 2)
            self.connect_path.lineTo(50, 50 - line_width / 2)
            self.connect_path.lineTo(50, 50 + line_width / 2)
            self.connect_path.lineTo(70, 50 + line_width / 2)
            self.connect_path.lineTo(70, 50 - line_width / 2)

            self.connect_node_path = QPainterPath()
            self.connect_node_path.addEllipse(QPointF(50, 50), 5, 5)
            self.connect_node_stroke = stroker.createStroke(self.connect_node_path)

        self.path = QPainterPath()
        self.path.addPath(self.symbol_path)
        self.path.addPath(self.symbol_path_stroke)
        self.path.addPath(self.connect_path)
        self.path.addPath(self.connect_node_path)
        self.path.addPath(self.connect_node_stroke)

        stroker.setWidth(10)
        path_stroker = stroker.createStroke(self.path)
        self.path.addPath(path_stroker)
        self.path.translate(-self.width / 2, -self.height / 2)
        self.setPath(self.path)

        self.label = defaultLabel
        self.textItem = DiagramTextItem(self.label)
        self.textItem.lost_focus.connect(self.editor_lost_focus)
        self.textItem.setParentItem(self)
        parentPos: QPointF = self.pos()
        boundingRect: QRectF = self.textItem.boundingRect()
        if isInputNode:
            translation = QPointF(25 + boundingRect.width() / 2, boundingRect.height() / 2)
        else:
            translation = QPointF(-25 + boundingRect.width() / 2, boundingRect.height() / 2)
        self.textItem.setPos(parentPos - translation)

    def getNodeScenePos(self, nodeType: NodeType = None) -> QPointF:
        if self.isInputNode:
            return self.mapToScene(15, 0)
        else:
            return self.mapToScene(-15, 0)

    # def paint(self, painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem, widget: Optional[PySide6.QtWidgets.QWidget] = ...) -> None:
    #     painter.translate(-self.width / 2, -self.height / 2)
    #     self._draw(painter)

    def _draw(self, painter: QPainter):
        painter.fillPath(self.symbol_path, QColor(Qt.yellow))
        painter.fillPath(self.symbol_path_stroke, QColor(Qt.black))
        painter.fillPath(self.connect_path, QColor(Qt.black))
        painter.fillPath(self.connect_node_path, QColor(Qt.green))
        painter.fillPath(self.connect_node_stroke, QColor(Qt.black))
        # super(SourceLogicGateItem, self).paint(painter, QStyleOptionGraphicsItem())

    def editor_lost_focus(self, item: QGraphicsTextItem):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        # If the input label is empty
        if not SourceLogicGateItem.isValidLabel(item.toPlainText()):
            item.setPlainText(self.label)

        self.label = item.toPlainText()

    @staticmethod
    def isValidLabel(label: str) -> bool:
        if len(label) == 0 or len(label) > 1:
            return False
        return label[0].isalpha()


class LineItem(LogicGateItem):
    def __init__(self, startItem: LogicGateItem, startNodeType: NodeType,
                 endItem: LogicGateItem, endNodeType: NodeType):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setZValue(1)
        self._start_item = startItem
        self._start_node_type = startNodeType

        self._end_item = endItem
        self._end_node_type = endNodeType

        self.setPen(QPen(QColor(Qt.red), 5))

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        startPos = LineItem.getPos(self._start_item, self._start_node_type)
        endPos = LineItem.getPos(self._end_item, self._end_node_type)
        path = LineItem.getZigZagLine(startPos, endPos)
        self.setPath(path)
        super(LineItem, self).paint(painter, option, widget)

    @staticmethod
    def getPos(node: LogicGateItem, nodeType: NodeType):
        return node.getNodeScenePos(nodeType)

    @staticmethod
    def isValidConnection(startNodeType: NodeType, endNodeType: NodeType):
        return not ((startNodeType.isInputNode() and endNodeType.isInputNode())
                    or (startNodeType.isOutputNode() and endNodeType.isOutputNode()))

    @staticmethod
    def getZigZagLine(start: QPointF, end: QPointF) -> QPainterPath:
        middle_x = (start.x() + end.x()) / 2
        path = QPainterPath()
        pathArr = [QPointF(middle_x, start.y()), QPointF(middle_x, end.y()), end]
        path.moveTo(start)
        for e in pathArr:
            path.lineTo(e)
        return path
