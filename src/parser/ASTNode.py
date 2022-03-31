from random import randint
from typing import List

from LogicTypes import LogicGateItem, LogicGateType, NodeType, ConsoleData


class Generator:
    _node_id: int = -1

    def genNodeId(self):
        self._node_id += 1
        return self._node_id

    def genSymbol(self):
        h = randint(0, 999)
        return chr(ord('A') + h % 26)

    def genOpLabel(self, symbolType: LogicGateType):
        if symbolType == LogicGateType.AND:
            return "&"
        elif symbolType == LogicGateType.OR:
            return "|"
        elif symbolType == LogicGateType.NOT:
            return "~"
        else:
            return symbolType.name

    def genLabel(self, type: LogicGateType):
        if type == LogicGateType.INPUT_NODE or type == LogicGateType.OUTPUT_NODE:
            return self.genSymbol()
        return self.genOpLabel(type)


class LogicSymbolNode(LogicGateItem):
    def __init__(self, nodeId: int, symbolType, label):
        self.node_id = nodeId
        self.symbol_type = symbolType
        self.label = label

        # important: used to trace ui
        self.parent = []
        self.leans = []

        # important: used to trace value in truth table
        self.col = []

        # if AND, OR gate, then we have both left and right child
        # if not gate, then only leftChild
        # if output symbol, then only leftChild
        # if input symbol, then both child should be None
        self.leftChild: int = -1
        self.rightChild: int = -1


# V2.0 我打算在这里使用COMP0005的图论算法
# 这里使用Directed Graph
class ASTGraph:
    AND = '&'
    OR = '|'
    NOT = '~'
    # 运算符元组
    OPERATORS = (AND, OR, NOT, '(', ')')
    # 优先级
    PRIORITY = dict([
        (OR, 1),
        (AND, 1),
        (NOT, 2),
    ])

    def __init__(self):
        self.inputNodeIndex = 0
        self.marked = None
        self.table = []
        self.root = None
        self.inputNodeNum = 0
        self.adjList: List[LogicSymbolNode] = []
        self.generator = Generator()

    def addNode(self, item: LogicGateItem):
        item_id = item.node_id
        t = LogicGateType[item.symbolName]

        if t == LogicGateType.OUTPUT_NODE:
            if self.root is None:
                self.root = item
            else:
                raise Exception("You cannot add two root node, error node id: " + str(item_id))

        if t == LogicGateType.INPUT_NODE or t == LogicGateType.OUTPUT_NODE:
            newNode = LogicSymbolNode(item_id, t, item.label)
        else:
            newNode = LogicSymbolNode(item_id, t, self.generator.genLabel(t))

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
        if inputNodeType.name == NodeType.LeftNode.name or inputNodeType.name == NodeType.INSourceNode.name:
            inputNode.leftChild = outputItem.node_id
        elif inputNodeType.name == NodeType.RightNode.name:
            inputNode.rightChild = outputItem.node_id
        else:
            raise Exception("Invalid Argument: Cannot found any input node from " + inputNodeType.name)

        if LogicGateType[outputItem.symbolName] == LogicGateType.INPUT_NODE:
            self.inputNodeNum += 1

    # We assume both item is existed in the graph
    def removeRelation(self, item1: LogicGateItem, item2: LogicGateItem):

        s1 = self.adjList[item1.node_id]
        s2 = self.adjList[item2.node_id]

        if s1.symbol_type.isSourceNode() or s1.symbol_type.isSourceNode():
            self.inputNodeNum -= 1

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

        self.toExpression()

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

    def changeNodeLabel(self, node_id: int, new_label: str):
        if 0 <= node_id < len(self.adjList) and self.adjList[node_id] is not None:
            self.adjList[node_id].label = new_label

    def checkValid(self, n: LogicSymbolNode = None) -> bool:
        if n is None:
            optionalN = self.findRoot()
            if optionalN is None:
                return False
            n = optionalN

        isValid = True

        # check left tree first
        if n.leftChild != -1:
            isValid = self.checkValid(self.adjList[n.leftChild])

        if n.symbol_type != LogicGateType.INPUT_NODE and n.symbol_type != LogicGateType.OUTPUT_NODE:
            if n.leftChild == -1 or n.rightChild == -1 and (n.symbol_type == LogicGateType.AND or n.symbol_type == LogicGateType.OR):
                isValid = False
            if n.leftChild == -1 and n.symbol_type == LogicGateType.NOT:
                isValid = False

        # check right tree then
        if n.rightChild != -1:
            isValid = self.checkValid(self.adjList[n.rightChild])

        return isValid

    def toExpression(self) -> ConsoleData:
        data = ConsoleData()

        if not self.checkValid():
            return data

        root = self.findRoot()
        if root is None or root.leftChild == -1:
            return data

        self.table: List[List[int]] = []
        self.marked: List[bool] = [False for _ in self.adjList]
        self.inputNodeIndex = 0

        op1 = self.adjList[root.leftChild]
        data.label = root.label

        expr = self.into(op1, root=True)
        data.expression = expr

        data.truthTable = self.table

        return data

    def findRoot(self):
        for elem in self.adjList:
            if elem.symbol_type == LogicGateType.OUTPUT_NODE:
                return elem
        return None

    @staticmethod
    def calcAnd(x, y):
        if x == 1 and y == 1:
            return 1
        else:
            return 0

    @staticmethod
    def calcOr(x, y):
        if x == 0 and y == 0:
            return 0
        return 1

    @staticmethod
    def calcNot(x):
        if x == 1:
            return 0
        return 1

    def into(self, n: LogicSymbolNode, root=False) -> str:
        res = ""
        lcol = []
        rcol = []

        # calc truth table col for source node
        if not self.marked[n.node_id] and n.symbol_type == LogicGateType.INPUT_NODE:
            n.col = []
            n.col.append(n.label)
            interval = 2 ** (self.inputNodeNum - self.inputNodeIndex - 1)
            startVal = 1
            for i in range(2 ** self.inputNodeNum):
                if i % interval == 0:
                    startVal = ASTGraph.calcNot(startVal)
                n.col.append(startVal)
            self.table.insert(0, n.col)
            self.inputNodeIndex += 1
            self.marked[n.node_id] = True

        # not case directly return
        if n.symbol_type == LogicGateType.NOT:
            if n.leftChild != -1:
                # first carry calculation of below nodes
                l = self.adjList[n.leftChild]
                assert l is not None
                genExpr = self.into(l)
                if l.leftChild == -1 and l.rightChild == -1:
                    genExpr = n.label + l.label
                else:
                    genExpr = n.label + "(" + genExpr + ")"

                # deal with not node truth table col directly
                genCol = [genExpr]
                for e in l.col[1:]:
                    genCol.append(ASTGraph.calcNot(e))
                n.col = genCol
                self.table.append(genCol)

                return genExpr
            else:
                raise Exception("Invalid Expression")

        # normal left handling
        if n.leftChild != -1:
            # carry below nodes calculations first
            leftChild = self.adjList[n.leftChild]
            if leftChild.leftChild == -1 and leftChild.rightChild == -1:
                res += self.into(leftChild)
            else:
                res += "(" + self.into(leftChild) + ")"
            # then save lcol for leftChild without label
            lcol = leftChild.col[1:]

        res += " " + str(n.label) + " "

        if n.rightChild != -1:
            # first carry calculation
            rightChild = self.adjList[n.rightChild]
            if rightChild.leftChild == -1 and rightChild.rightChild == -1:
                res += self.into(rightChild)
            else:
                res += "(" + self.into(rightChild) + ")"
            # then save the truth table val only for right child
            rcol = rightChild.col[1:]

        # handle AND OR truth table calc, len(lcol) == len(rcol)
        if n.symbol_type != LogicGateType.INPUT_NODE:
            n.col = []
            n.col.append(res)  # append label
            for i in range(len(lcol)):
                if n.symbol_type == LogicGateType.AND:
                    n.col.append(ASTGraph.calcAnd(lcol[i], rcol[i]))
                elif n.symbol_type == LogicGateType.OR:
                    n.col.append(ASTGraph.calcOr(lcol[i], rcol[i]))
            self.table.append(n.col)

        return res

    # 依次压栈并追加到后缀表达式，直到遇到左括号为止
    @staticmethod
    def pop_left_bracket(postfix, operators):
        while operators:
            operator = operators.pop()
            if operator == '(':
                break
            else:
                postfix.append(operator)

    # 比较优先级并进行相应操作
    @staticmethod
    def compare_and_pop(i, postfix, operators):
        if len(operators) == 0:
            operators.append(i)
            return
        while operators:
            operator = operators.pop()
            if operator == '(':
                operators += ['(', i]
                return
            elif ASTGraph.PRIORITY[i] > ASTGraph.PRIORITY[operator]:
                operators += [operator, i]
                return
            else:
                postfix.append(operator)
                operators.append(i)
                return

    @staticmethod
    # 弹出所有剩余的运算符，追加到后缀表达式，完成最后的逆波兰式
    def pop_rest(postfix, operators):
        while operators:
            postfix.append(operators.pop())

    @staticmethod
    # 判断是否为英文字母输入
    def isInputLexem(lex: str):
        return lex.isalpha()

    @staticmethod
    # 将中缀表达式转换为后缀表达式
    def infix_to_postfix(infix: List[str]) -> List[str]:
        postfix = []
        operators = []
        print(infix)
        # 检查中缀表达式合法性
        for i in infix:
            # 如果是字母那么就加入到postfix列表中
            if ASTGraph.isInputLexem(i) and (i != "(") and (i != ")"):
                postfix.append(i)
            # 如果是运算符就加入到 operators 列表中
            elif i in ASTGraph.OPERATORS:
                # 左括号处理
                if i == '(':
                    operators.append(i)
                # 右括号处理
                elif i == ')':
                    ASTGraph.pop_left_bracket(postfix, operators)
                # 普通运算符处理
                else:
                    ASTGraph.compare_and_pop(i, postfix, operators)

        ASTGraph.pop_rest(postfix, operators)

        return postfix

    # 逆波兰式 -> parse tree in list form
    def addGraph(self, lexerList, label: str) -> None:
        s = []
        for c in lexerList:
            # 如果是输入字母
            if ASTGraph.isInputLexem(c):
                self.inputNodeNum += 1
                node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.INPUT_NODE, c)
                node.leftChild = -1
                node.rightChild = -1
                self.adjList.append(node)
                s.append(node)

            # 如果是运算符
            elif c in ASTGraph.OPERATORS:

                if c == ASTGraph.AND:
                    right = s.pop()
                    left = s.pop()
                    node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.AND,
                                           self.generator.genLabel(LogicGateType.AND))
                    node.leftChild = left.node_id
                    node.rightChild = right.node_id
                    s.append(node)
                    self.adjList.append(node)

                elif c == ASTGraph.OR:
                    right = s.pop()
                    left = s.pop()
                    node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.OR,
                                           self.generator.genLabel(LogicGateType.OR))
                    node.leftChild = left.node_id
                    node.rightChild = right.node_id
                    s.append(node)
                    self.adjList.append(node)

                elif c == ASTGraph.NOT:
                    left = s.pop()
                    node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.NOT,
                                           self.generator.genLabel(LogicGateType.NOT))
                    node.leftChild = left.node_id
                    node.rightChild = -1
                    s.append(node)
                    self.adjList.append(node)
            else:
                raise Exception("Unsupported Operator")
        if len(self.adjList) == 0:
            return
        rootNode = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.OUTPUT_NODE, label)
        rootNode.leftChild = self.adjList[-1].node_id
        self.adjList.append(rootNode)

    @staticmethod
    def lexer(expr: str):
        lst = []
        for e in expr:
            if e != " ":
                lst.append(e)
        return lst

    # 整合AST生成的两个步骤
    @staticmethod
    def fromExpression(expr: str, label: str):
        ast = ASTGraph()
        lexerList = ASTGraph.lexer(expr)
        postfixList = ASTGraph.infix_to_postfix(lexerList)
        print(postfixList)
        ast.addGraph(postfixList, label)
        return ast


    # # 逆波兰式 -> parse tree in list form
    # def addGraph(self, lexerList, label: str) -> None:
    #     s = []
    #     for c in lexerList:
    #         # 如果是输入字母
    #         if ASTGraph.isInputLexem(c):
    #             self.inputNodeNum += 1
    #             node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.INPUT_NODE, c)
    #             node.leftChild = -1
    #             node.rightChild = -1
    #             self.adjList.append(node)
    #             s.append(node)
    #
    #         # 如果是运算符
    #         elif c in ASTGraph.OPERATORS:
    #
    #             if c == ASTGraph.AND:
    #                 left = self.adjList.pop()
    #                 right = self.adjList.pop()
    #
    #                 if left.symbol_type == LogicGateType.NOT:
    #                     NOT_child = right
    #                     right = self.adjList.pop()
    #                     node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.AND,
    #                                            self.generator.genLabel(LogicGateType.AND))
    #                     node.leftChild = left.node_id
    #                     node.rightChild = right.node_id
    #                     self.adjList.append(right)
    #                     self.adjList.append(NOT_child)
    #                     self.adjList.append(node)
    #
    #                 else:
    #                     node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.AND,
    #                                            self.generator.genLabel(LogicGateType.AND))
    #                     node.leftChild = left.node_id
    #                     node.rightChild = right.node_id
    #                     self.adjList.append(left)
    #                     self.adjList.append(right)
    #                     self.adjList.append(node)
    #
    #             elif c == ASTGraph.OR:
    #                 left = self.adjList.pop()
    #                 right = self.adjList.pop()
    #
    #                 if left.symbol_type == LogicGateType.NOT:
    #                     NOT_child = right
    #                     right = self.adjList.pop()
    #                     node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.OR,
    #                                            self.generator.genLabel(LogicGateType.OR))
    #                     node.leftChild = left.node_id
    #                     node.rightChild = right.node_id
    #                     self.adjList.append(right)
    #                     self.adjList.append(NOT_child)
    #                     self.adjList.append(left)
    #                     self.adjList.append(node)
    #
    #                 else:
    #                     node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.OR,
    #                                            self.generator.genLabel(LogicGateType.OR))
    #                     node.leftChild = left.node_id
    #                     node.rightChild = right.node_id
    #                     self.adjList.append(left)
    #                     self.adjList.append(right)
    #                     self.adjList.append(node)
    #
    #             elif c == ASTGraph.NOT:
    #                 left = self.adjList.pop()
    #                 node = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.NOT,
    #                                        self.generator.genLabel(LogicGateType.NOT))
    #                 node.leftChild = left.node_id
    #                 node.rightChild = -1
    #                 self.adjList.append(left)
    #                 self.adjList.append(node)
    #         else:
    #             raise Exception("Unsupported Operator")
    #     if len(self.adjList) == 0:
    #         return
    #     rootNode = LogicSymbolNode(self.generator.genNodeId(), LogicGateType.OUTPUT_NODE, label)
    #     rootNode.leftChild = self.adjList[-1].node_id
    #     self.adjList.append(rootNode)