from jugri import to_df, toDF
import numpy as np
import pandas as pd
import unittest
from gremlin_python.process.graph_traversal import GraphTraversal
from gremlin_python.structure.graph import Vertex, Path


def wrap_content_as_traversal(*content):
    mockTraversal = GraphTraversal.__new__(GraphTraversal)
    mockTraversal.toList = lambda: list(content)
    return mockTraversal


class TestPandification(unittest.TestCase):

    def testNestedFields(self):
        traversal_result = [{"T.id":"T1","T.label":"node" },
                      {"T.id":"T2","T.label":"node" , "nested": {"field1": [0]}},
                      {"T.id":"T3","T.label":"node", "nested": {"field1": [1]}},
                      {"T.id":"T4","T.label":"node" }]
        df = to_df(traversal_result)
        test_df = pd.DataFrame(columns=['T.id', 'T.label', 'nested.field1'],
                               data=[['T1', 'node', np.nan],
                                     ['T2', 'node', 0.0],
                                     ['T3', 'node', 1.0],
                                     ['T4', 'node', np.nan]],
                               index=[0, 1, 2, 3])

        self.assertTrue(test_df.equals(df)
                             , "Dictionary with nested field does not transform properly.")

    def testEmptyResult(self):
        traversal_result = []
        df = to_df(traversal_result)
        self.assertTrue(pd.DataFrame().equals(df), "Empty result does not yield empty DataFrame.")

    def testToListCall(self):
        traversal = wrap_content_as_traversal(Vertex("v1"), Vertex("v2"), Vertex("v3"))
        df = to_df(traversal)
        self.assertEqual(len(df.index), 3, "DataFrame is not populated properly.")

    def testColumns(self):
        traversal = wrap_content_as_traversal(Vertex("v1"), Vertex("v2"), Vertex("v3"))
        df = to_df(traversal)
        self.assertListEqual(df.columns.values.tolist(), ['id', 'label'], "Incorrect field names extracted.")

    def testProfiling(self):
        data = [{'@type': 'g:TraversalMetrics',
                 '@value': {'dur': 0.8397500000000001,
                            'metrics': [{'@type': 'g:Metrics',
                                         '@value': {'dur': 0.210785,
                                                    'counts': {'traverserCount': 1, 'elementCount': 1},
                                                    'name': 'NeptuneGraphQueryStep(Vertex)',
                                                    'annotations': {'percentDur': 25.10092289371837},
                                                    'id': '8.0.0()'}},
                                        {'@type': 'g:Metrics',
                                         '@value': {'dur': 0.628965,
                                                    'counts': {'traverserCount': 1, 'elementCount': 1},
                                                    'name': 'PropertyMapStep(value)',
                                                    'annotations': {'percentDur': 74.89907710628164},
                                                    'id': '4.0.0()'}}]}}]
        df = to_df(data)
        self.assertAlmostEqual(df.iloc[0,0],25.10092289371837, 5,"DataFrame format is not correct.")
        self.assertAlmostEqual(df.loc[1,"annotations.percentDur"], 74.89908,4, "Profile data not correctly flattened.")

    def testNoProfiling(self):
        data = [{'@type': 'g:TraversalMetrics',
                 '@value': {'dur': 0.8397500000000001,
                            'metrics': [{'@type': 'g:Metrics',
                                         '@value': {'dur': 0.210785,
                                                    'counts': {'traverserCount': 1, 'elementCount': 1},
                                                    'name': 'NeptuneGraphQueryStep(Vertex)',
                                                    'annotations': {'percentDur': 25.10092289371837},
                                                    'id': '8.0.0()'}},
                                        {'@type': 'g:Metrics',
                                         '@value': {'dur': 0.628965,
                                                    'counts': {'traverserCount': 1, 'elementCount': 1},
                                                    'name': 'PropertyMapStep(value)',
                                                    'annotations': {'percentDur': 74.89907710628164},
                                                    'id': '4.0.0()'}}]}}]
        df = to_df(data, detect_profiling=False)
        self.assertEqual(df.loc[0,'@type'],'g:TraversalMetrics',"DataFrame format is not correct.")

    def testDictList(self):
        data = [{'Cluster': [
                             '_id',
                             'cluster.prop1.value',
                             '_label'],
                 'Organization': ['org.prop2.value',
                                  '_id',
                                  '_label'],
                 'Address': ['addr.prop1.value',
                             'addr.prop2.value',
                             '_label',
                             '_id'],
                 'Job': [
                         '_id',
                         '_label'],
                 'Person': ['cluster.prop1.value',
                            'cluster.prop2.value',
                            'cluster.prop3.value',
                            '_id',
                            '_label'],
                 'Source': [
                            '_id'],
                'Nothing': []
        }]
        df = to_df(data)
        self.assertEqual(df['Nothing'].values[0], None)
        self.assertEqual(df['Source'].values[0], '_id')
        self.assertListEqual(df['Job'].values[0], [
            '_id',
            '_label'])


