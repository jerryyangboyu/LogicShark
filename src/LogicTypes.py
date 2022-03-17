from enum import Enum
from typing import Protocol, List


class LogicGateItem(Protocol):
    node_id: int
    symbolName: str
    label: str = ""


class LogicGateType(Enum):
    AND, OR, NOT, INPUT_NODE, OUTPUT_NODE = range(5)


class NodeType(Enum):
    NoneNode, LeftNode, RightNode, TopNode, INSourceNode, OUTSourceNode = range(6)

    def isInputNode(self):
        return self.value == NodeType.LeftNode.value or self.value == NodeType.RightNode.value \
               or self.value == NodeType.INSourceNode.value

    def isOutputNode(self):
        return self.value == NodeType.TopNode.value or self.value == NodeType.OUTSourceNode.value


class ConsoleData:
    label: str = ""
    expression: str = ""
    truthTable: List[List[str]] = None
