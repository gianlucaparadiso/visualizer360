from structures.node import Node
from structures.edge import Edge
from collections import OrderedDict


class Model:
    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.nodeDic = OrderedDict()

    def resetModel(self):
        self.nodes.clear()
        self.edges.clear()
        self.nodeDic.clear()

    def createModel(self, data):
        pass

    def addNode(self, node: Node):
        self.nodes.append(node)

        self.nodeDic[node.idx] = node

    def addEdge(self, edge: Edge):
        self.edges.append(edge)
