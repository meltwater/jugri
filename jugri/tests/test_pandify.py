from jugri import toDF
import unittest
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.structure.graph import Vertex, Path


def wrapContentAsTraversal(*content):
    mockTraversal = GraphTraversal.__new__(GraphTraversal)
    mockTraversal.toList = lambda: list(content)
    return mockTraversal


class TestPandification(unittest.TestCase):

    def testToListCall(self):
        traversal = wrapContentAsTraversal(Vertex("v1"), Vertex("v2"), Vertex("v3"))
        df = toDF(traversal)
        self.assertEqual(len(df.index), 3, "DataFrame is not populated properly.")

    def testColumns(self):
        traversal = wrapContentAsTraversal(Vertex("v1"), Vertex("v2"), Vertex("v3"))
        df = toDF(traversal)
        self.assertListEqual(df.columns.values.tolist(), ['id', 'label'], "Incorrect field names extracted.")


