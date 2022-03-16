from random import randint
from typing import List, Tuple

from LogicTypes import LogicGateItem, LogicGateType, NodeType

node_id: int = 0


def genNodeId():
    global node_id
    node_id += 1
    return node_id


def genSymbol():
    h = randint(0, 999)
    return chr(ord('A') + h % 26)


def genOpLabel(symbolType: LogicGateType):
    if symbolType == LogicGateType.AND:
        return "&"
    elif symbolType == LogicGateType.OR:
        return "|"
    elif symbolType == LogicGateType.NOT:
        return "~"
    else:
        return symbolType.name


class LogicSymbolNode(LogicGateItem):
    def __init__(self, nodeId: int, symbolType, label=None):
        self.node_id = nodeId
        self.symbol_type = symbolType
        self.label = genOpLabel(symbolType) if label is None else label

        # important: used to trace ui
        self.parent = []
        self.leans = []

        # if AND, OR gate, then we have both left and right child
        # if not gate, then only leftChild
        # if output symbol, then only leftChild
        # if input symbol, then both child should be None
        self.leftChild: int = -1
        self.rightChild: int = -1


# V2.0 我打算在这里使用COMP0005的图论算法
# 这里使用Directed Graph
class ASTGraph:
    def __init__(self):
        self.adjList: List[LogicSymbolNode] = []

    def addNode(self, item: LogicGateItem):
        item_id = item.node_id
        if item.symbolName == LogicGateType.INPUT_NODE.name or item.symbolName == LogicGateType.OUTPUT_NODE.name:
            newNode = LogicSymbolNode(item_id, LogicGateType[item.symbolName], item.label)
        else:
            newNode = LogicSymbolNode(item_id, LogicGateType[item.symbolName])
        # if id exceed, then expand the list
        # note that id increase linearly, so it won't cost much memory
        if item_id >= len(self.adjList):
            distance = item_id - len(self.adjList) + 1
            newArr = [None] * distance
            newArr[-1] = newNode
            self.adjList.extend(newArr)
        else:
            self.adjList[item_id] = newNode

    # We assume below is not satisfied
    # (fromNode.isInputNode() and toNode.isInputNode()) or (toNode.isOutputNode() and toNode.isOutputNode())
    def addRelation(self, fromItem: LogicGateItem, fromNode: NodeType, toItem: LogicGateItem, toNode: NodeType):
        # Check which one is real input node
        inputNode: LogicSymbolNode = None
        outputItem = None
        inputNodeType = None
        if fromNode.isInputNode():
            inputNode = self.adjList[fromItem.node_id]
            if inputNode is not None:
                outputItem = toItem
                inputNodeType = fromNode
        else:
            inputNode = self.adjList[toItem.node_id]
            if inputNode is not None:
                outputItem = fromItem
                inputNodeType = toNode
        if inputNode is None:
            raise Exception("Invalid Argument: Cannot found input Node")

        # check if outputNode exists and get index
        if self.adjList[outputItem.node_id] is None:
            raise Exception("Invalid Argument: Cannot found output Node")

        # associate the output node to input node
        if inputNodeType == NodeType.LeftNode or inputNodeType == NodeType.INSourceNode:
            s: LogicGateType = LogicGateType[outputItem.symbolName]
            inputNode.leftChild = outputItem.node_id
        elif inputNodeType == NodeType.RightNode:
            inputNode.rightChild = outputItem.node_id
        else:
            raise Exception("Invalid Argument: Cannot found any input node from " + inputNodeType.name)

    # We assume both item is existed in the graph
    def removeRelation(self, item1: LogicGateItem, item2: LogicGateItem):

        s1 = self.adjList[item1.node_id]
        s2 = self.adjList[item2.node_id]

        if s1 is None or s2 is None:
            return

        if s1.leftChild == item2.node_id:
            s1.leftChild = -1
        elif s1.rightChild == item2.node_id:
            s2.rightChild = -1
        elif s2.leftChild == item1.node_id:
            s2.leftChild = -1
        elif s2.rightChild == item1.node_id:
            s2.rightChild = -1
        else:
            raise Exception("No relationship found between two nodes")

    def removeNode(self, item: LogicGateItem):
        if item.node_id < len(self.adjList):
            self.adjList[item.node_id] = None

    # This debug function shows how to iterate the whole AST
    def printRelationship(self):
        # Find the root Node
        roots = []
        for e in self.adjList:
            if e is not None and e.symbol_type == LogicGateType.OUTPUT_NODE:
                roots.append(e)

        SearchPaths = ASTGraph.BreathFirstSearchPaths(self)
        for root in roots:
            SearchPaths.bfs(root)

        self.toExpressions()

    class BreathFirstSearchPaths:
        def __init__(self, G):
            self.distToSource = [-1 for i in range(len(G.adjList))]
            self.current_height = 0
            self.G = G

        def bfs(self, s: LogicSymbolNode):
            q: List[LogicSymbolNode] = [s]
            self.distToSource[s.node_id] = 0
            while len(q) != 0:
                v = q.pop(0)
                if self.current_height + 1 == self.distToSource[v.node_id]:
                    print()
                    self.current_height += 1
                print("[%d, %s]" % (v.node_id, v.label), end="")

                if v.leftChild != -1:
                    w = v.leftChild
                    if self.distToSource[w] == -1:
                        q.append(self.G.adjList[w])
                        self.distToSource[w] = self.distToSource[v.node_id] + 1
                if v.rightChild != -1:
                    w = v.rightChild
                    if self.distToSource[w] == -1:
                        q.append(self.G.adjList[w])
                        self.distToSource[w] = self.distToSource[v.node_id] + 1

    # TODO @Qiren Dong, to check whether the graph contains correct expression
    def checkValid(self) -> bool:
        # write your code here
        return True

    def toExpressions(self) -> Tuple[List[str], List[str]]:
        exprs = []
        labels = []
        roots = self.findRoot()
        for root in roots:
            op1 = self.adjList[root.leftChild]
            labels.append(root.label)
            exprs.append(self.into(op1))
        return exprs, labels

    def findRoot(self):
        roots = []
        for e1 in self.adjList:
            if e1 is None:
                continue
            isRoot = True
            for e2 in self.adjList:
                if e2 is None:
                    continue
                if e1.node_id == e2.leftChild or e1.node_id == e2.rightChild:
                    isRoot = False
            if isRoot:
                roots.append(e1)
        return roots

    def into(self, n: LogicSymbolNode) -> str:
        res = ""
        if n.symbol_type == LogicGateType.NOT:
            if n.leftChild != -1:
                return n.label + "(" + self.into(self.adjList[n.leftChild]) + ")"
            else:
                raise Exception("Invalid Expression")
        if n.leftChild != -1:
            leftChild = self.adjList[n.leftChild]
            if leftChild.leftChild == -1 and leftChild.rightChild == -1:
                res += self.into(leftChild)
            else:
                res += "(" + self.into(leftChild) + ")"
        res += " " + str(n.label) + " "
        if n.rightChild != -1:
            rightChild = self.adjList[n.rightChild]
            if rightChild.leftChild == -1 and rightChild.rightChild == -1:
                res += self.into(rightChild)
            else:
                res += "(" + self.into(rightChild) + ")"
        return res

    # TODO @Qiren Dong, generate This graph from a expression, [Optional]
    # The graph may only contain one tree
    # This static method returns a ASTGraph object to CoreUI module
    @staticmethod
    def fromExpression(expression: str):
        return ASTGraph()




