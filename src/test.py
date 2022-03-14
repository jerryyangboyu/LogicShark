from ast import ASTGraph, genNodeId
from logicTypes import NodeType, LogicGateItem, LogicGateType


class DummyLogicGateItem(LogicGateItem):
    def __init__(self, symbolType: LogicGateType, label=None):
        self.node_id = genNodeId()
        self.symbolName = symbolType.name
        self.label = self.symbolName if label is None else label


def testNodeType():
    assert not NodeType.TopNode.isInputNode()


def testASTGraphVisualize():
    g = ASTGraph()
    n1 = DummyLogicGateItem(LogicGateType.OUTPUT_NODE, label="Y")
    n2 = DummyLogicGateItem(LogicGateType.AND)
    n3 = DummyLogicGateItem(LogicGateType.NOT)
    n4 = DummyLogicGateItem(LogicGateType.INPUT_NODE, label="A")
    n5 = DummyLogicGateItem(LogicGateType.INPUT_NODE, label="B")
    n6 = DummyLogicGateItem(LogicGateType.INPUT_NODE, label="C")
    n7 = DummyLogicGateItem(LogicGateType.OR)

    g.addNode(n1, label=n1.label)
    g.addNode(n2)
    g.addNode(n3)
    g.addNode(n4, label=n4.label)
    g.addNode(n5, label=n5.label)
    g.addNode(n6, label=n6.label)
    g.addNode(n7)

    g.addRelation(n7, NodeType.TopNode, n1, NodeType.INSourceNode)
    g.addRelation(n2, NodeType.TopNode, n7, NodeType.LeftNode)
    g.addRelation(n3, NodeType.TopNode, n7, NodeType.RightNode)
    g.addRelation(n4, NodeType.OUTSourceNode, n2, NodeType.LeftNode)
    # g.addRelation(n2, NodeType.TopNode, n4, NodeType.TopNode)
    g.addRelation(n5, NodeType.OUTSourceNode, n2, NodeType.RightNode)
    g.addRelation(n6, NodeType.OUTSourceNode, n3, NodeType.LeftNode)

    # g.removeRelation(n2, n7)
    # g.removeRelation(n4, n2)
    # g.removeRelation(n5, n2)
    # g.removeNode(n2)

    print(g.toExpressions())
    # g.printRelationship()


    # test simple root conenct case
    # g = ASTGraph()
    # g.addNode(n1)
    # g.addNode(n7)
    # g.addRelation(n7, NodeType.TopNode, n1, NodeType.INSourceNode)
    #
    # g.removeRelation(n7, n1)
    # g.removeNode(n7)

    # g.printRelationship()


if __name__ == '__main__':
    testASTGraphVisualize()
