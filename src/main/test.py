from enum import Enum


class NodeType(Enum):
    NoneNode, LeftNode, RightNode, TopNode = range(4)

    def isInputNode(self):
        return self.value == NodeType.LeftNode.value or self.value == NodeType.RightNode.value

    def isOutputNode(self):
        return self.value == NodeType.TopNode.value


if __name__ == '__main__':
    print(NodeType.TopNode.isInputNode())
