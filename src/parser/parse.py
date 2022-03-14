from enum import Enum

class InvalidOperatorException(Exception):
    def __init__(self):
        self.message = "invalid operator"

    def __str__(self):
        return self.message

class SymbolType(Enum):
    SCALAR = 1
    OP = 2

class ValueType(Enum):
    TRUE = 1
    FALSE = 0

class OperatorType(Enum):
    NOT = 1
    AND = 2
    OR = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5

class Node:
    """
    a + b => true
           +(true)
    a(true)   b(true)
    """
    def __init__(self, left, right, val, symbolType):
        self.left = left
        self.right = right
        self.val = val
        self.symbolType = symbolType

class PeekIterator:
    def __init__(self, arr: str):
        self.tokens = [e for e in arr if e != ' ']
        self.index = 0
        self.l = len(self.tokens)

    def hasNext(self):
        return not self.index == self.l

    def next(self):
        if not self.hasNext():
            return None
        val = self.tokens[self.index]
        self.index += 1
        return val

    def peek(self):
        if not self.hasNext():
            return None
        return self.tokens[self.index + 1]

    def putBack(self):
        self.index -= 1


# construct the syntax tree by input code, if success return tree, if not, return None
def parse(code: str) -> Node:
    it = PeekIterator(code)


    while it.hasNext():
        val = it.peek()
        # a b c A B C
        if val.isalpha():


if __name__ == '__main__':
    it = PeekIterator("a & b | (c | d)")
    print(it.next())
    print(it.next())
    it.putBack()
    print(it.peek())
    print(it.next())
