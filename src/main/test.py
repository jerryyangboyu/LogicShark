from src.main.DiagramItem import ANDLogicGateItem, ORLogicGateItem, NOTLogicGateItem, SourceLogicGateItem
from src.main.ast import ASTGraph, genNodeId
from src.main.logicTypes import NodeType, LogicGateItem, LogicGateType


class DummyLogicGateItem(LogicGateItem):
    def __init__(self, symbolType: LogicGateType):
        self.node_id = genNodeId()
        self.symbolName = symbolType.name


def testNodeType():
    assert not NodeType.TopNode.isInputNode()


def testASTGraphVisualize():
    g = ASTGraph()
    n1 = DummyLogicGateItem(LogicGateType.OUTPUT_NODE)
    n2 = DummyLogicGateItem(LogicGateType.AND)
    n3 = DummyLogicGateItem(LogicGateType.NOT)
    n4 = DummyLogicGateItem(LogicGateType.INPUT_NODE)
    n5 = DummyLogicGateItem(LogicGateType.INPUT_NODE)
    n6 = DummyLogicGateItem(LogicGateType.INPUT_NODE)
    n7 = DummyLogicGateItem(LogicGateType.OR)

    g.addNode(n1)
    g.addNode(n2)
    g.addNode(n3)
    g.addNode(n4)
    g.addNode(n5)
    g.addNode(n6)
    g.addNode(n7)

    g.addRelation(n7, NodeType.TopNode, n1, NodeType.INSourceNode)
    g.addRelation(n2, NodeType.TopNode, n7, NodeType.LeftNode)
    g.addRelation(n3, NodeType.TopNode, n7, NodeType.RightNode)
    g.addRelation(n4, NodeType.OUTSourceNode, n2, NodeType.LeftNode)
    # g.addRelation(n2, NodeType.TopNode, n4, NodeType.TopNode)
    g.addRelation(n5, NodeType.OUTSourceNode, n2, NodeType.RightNode)
    g.addRelation(n6, NodeType.OUTSourceNode, n3, NodeType.LeftNode)

    g.removeRelation(n2, n7)
    g.removeRelation(n4, n2)
    g.removeRelation(n5, n2)
    g.removeNode(n2)

    # test simple root conenct case
    g = ASTGraph()
    g.addNode(n1)
    g.addNode(n7)
    g.addRelation(n7, NodeType.TopNode, n1, NodeType.INSourceNode)

    g.removeRelation(n7, n1)
    g.removeNode(n7)

    g.printRelationship()


if __name__ == '__main__':
    testASTGraphVisualize()
