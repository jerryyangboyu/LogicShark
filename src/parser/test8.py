# input:[(A AND B) AND C]
# output: Tree
# 此段为总代码，唯一缺陷在于生成波兰式这一步未能应对更多的corner case
# 逆波兰式生成代码还未来得及替换，lexima.py中才是这部分代码的最新内容。在这份版本中，已经解决了几个corner case，包括 A AND NOT NOT NOT B 和默认越前面优先级越大（没有括号的情况下）
# 唯一还未来得及解决的点在于括号不完整情况下如何填补括号，已经可以解决一些basic case，但是更复杂case有待商讨
# 另外，split函数还未替换，但是这段替换源代码已经在split.py中。
from tokenize import String
from typing import List

AND = 'AND'
OR = 'OR'
NOT = 'NOT'
# 运算符元组
OPERATORS = ('AND', 'OR', 'NOT', '(', ')')
# 优先级
PRIORITY = dict([
    ('OR', 1),
    ('AND', 1),
    ('NOT', 2),
])


# 依次压栈并追加到后缀表达式，直到遇到左括号为止
def pop_left_bracket(postfix, operators):
    while operators:
        operator = operators.pop()
        if operator == '(':
            break
        else:
            postfix.append(operator)


# 比较优先级并进行相应操作
def compare_and_pop(i, postfix, operators):
    if len(operators) == 0:
        operators.append(i)
        return
    while operators:
        operator = operators.pop()
        if operator == '(':
            operators += ['(', i]
            return
        elif PRIORITY[i] > PRIORITY[operator]:
            operators += [operator, i]
            return
        else:
            postfix.append(operator)
            operators.append(i)
            return


# 弹出所有剩余的运算符，追加到后缀表达式，完成最后的逆波兰式
def pop_rest(postfix, operators):
    while operators:
        postfix.append(operators.pop())


# 判断是否为英文字母输入
def is_input(input):
    if len(input) == 1:
        return True
    elif len(input) != 1:
        return False


# 将中缀表达式转换为后缀表达式
def infix_to_postfix(infix):
    infix = infix.split()
    postfix = []
    operators = []
    print(infix)
    # 检查中缀表达式合法性
    for i in infix:
        # 如果是字母那么就加入到postfix列表中
        if is_input(i) and (i != "(") and (i != ")"):
            postfix.append(i)
        # 如果是运算符就加入到 operators 列表中
        elif i in OPERATORS:
            # 左括号处理
            if i == '(':
                operators.append(i)
            # 右括号处理
            elif i == ')':
                pop_left_bracket(postfix, operators)
            # 普通运算符处理
            else:
                compare_and_pop(i, postfix, operators)

    pop_rest(postfix, operators)

    return postfix


class LogicSymbolNode():
    def __init__(self, nodeId: int, symbolType):
        self.node_id = nodeId
        self.symbol_type = symbolType
        self.leftchild: int = -1
        self.rightchild: int = -1


global index_item
index_item = 0


class ASTGraph():
    def __init__(self):
        self.adList: List[LogicSymbolNode] = []

    # 逆波兰式 -> parse tree in list form
    def addGraph(self, lexerList):
        global index_item
        index_item = 0
        lexerList = output.split()

        for split_product in lexerList:

            # 如果是输入字母
            if is_input(split_product):
                split_product_Object = LogicSymbolNode(index_item, "INPUT")
                index_item += 1
                split_product_Object.leftchild = None
                split_product_Object.rightchild = None
                self.adList.append(split_product_Object)

            # 如果是运算符
            elif split_product in OPERATORS:

                if split_product == 'AND':
                    left = self.adList.pop()
                    right = self.adList.pop()

                    if left.symbol_type == 'NOT':
                        NOT_child = right
                        right = self.adList.pop()
                        split_product_Object = LogicSymbolNode(index_item, "AND")
                        index_item += 1
                        split_product_Object.leftchild = left
                        split_product_Object.rightchild = right
                        self.adList.append(right)
                        self.adList.append(NOT_child)
                        self.adList.append(split_product_Object)

                    elif left.symbol_type != 'NOT':
                        split_product_Object = LogicSymbolNode(index_item, "AND")
                        index_item += 1
                        split_product_Object.leftchild = left
                        split_product_Object.rightchild = right
                        self.adList.append(right)
                        self.adList.append(left)
                        self.adList.append(split_product_Object)

                elif split_product == 'OR':
                    left = self.adList.pop()
                    right = self.adList.pop()

                    if left.symbol_type == 'NOT':
                        NOT_child = right
                        right = self.adList.pop()
                        split_product_Object = LogicSymbolNode(index_item, "OR")
                        index_item += 1
                        split_product_Object.leftchild = left
                        split_product_Object.rightchild = right
                        self.adList.append(right)
                        self.adList.append(NOT_child)
                        self.adList.append(left)
                        self.adList.append(split_product_Object)

                    elif left.symbol_type != 'NOT':
                        split_product_Object = LogicSymbolNode(index_item, "OR")
                        index_item += 1
                        split_product_Object.leftchild = left
                        split_product_Object.rightchild = right
                        self.adList.append(left)
                        self.adList.append(right)
                        self.adList.append(split_product_Object)

                elif split_product == 'NOT':
                    left = self.adList.pop()
                    split_product_Object = LogicSymbolNode(index_item, "NOT")
                    index_item += 1
                    split_product_Object.leftchild = left
                    split_product_Object.rightchild = None
                    self.adList.append(left)
                    self.adList.append(split_product_Object)

        print(self.adList)
        return self.adList

    # 字符流-》逆波兰式
    def postfix_produce(self, expr):

        infix = input('please input equation:')

        postfix = infix_to_postfix(infix)  # 转换成逆波兰式

        postfix = ' '.join(postfix)

        print(postfix)

        print(type(postfix))

        return postfix

    # 整合AST生成的两个步骤
    def integrate(self):
        self.addGraph(self.postfix_produce())

    # 测试
    def test(self):
        length_ASTGraph = len(self.adList)
        for component in self.adList:
            print(component.node_id, ' ', component, ' symbol type:', component.symbol_type,
                  ' leftchild:', component.leftchild, ' rightchild:', component.rightchild)


def main():
    TestGraph = ASTGraph()
    TestGraph.integrate()
    TestGraph.test()
    return


if __name__ == '__main__':
    main()
