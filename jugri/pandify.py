from gremlin_python.structure.graph import Element, Path
from gremlin_python.process.graph_traversal import GraphTraversal
import pandas as pd
import collections
import logging

logger = logging.getLogger(__name__)


def _flatten(d, parent_key='', sep='_'):
    """
    Flatten nested fields using recursive calls.
    :param d: dictionary
    :param parent_key: current key
    :param sep: key separator
    :return: flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def _get_singular(value):
    if type(value) is list:
        lv = len(value)
        if  lv == 1:
            return value[0]
        elif lv == 0:
            None
        else:
            return value
    else:
        return value


def toDF(*args, **kwargs):
    raise DeprecationWarning("to_df should be used instead.")
    to_df(args, kwargs)


def to_df(gremlin_traversal, keep_first_only=None, key_value_pairs=False, flatten_dict=True, auto_cardinality=True):
    # type: (bool, bool, bool, bool) -> pd.DataFrame
    """
    Converts a Gremlin Traversal to a Pandas DataFrame. It expects a traversal or a list of traversal results.
    :param gremlin_traversal: A gremlinpython graph traversal (e.g. g.V().limit(5))
            or a list (e.g. g.V().limit(5).toList())
    :param keep_first_only: Deprecated since v0.3. Conversion is automatic and can be turned off
            using the auto_cardinality option.
    :param key_value_pairs: Set it to True when a map is returned. The DataFrame will have only two columns: the key and
            the values.
    :param flatten_dict: Set it to True if you have nested fields in your results. The field name will automatically
            become the "." concatenated hierarchy of the names (e.g. start.date.month, end.date.year, etc.)
    :param auto_cardinality: Set it to False for better performance. Singe element arrays will be automatically
            converted into the first element.
    :return: Pandas DataFrame
    """
    if type(gremlin_traversal) is GraphTraversal:
        gremlin_traversal = gremlin_traversal.toList()
    if len(gremlin_traversal) == 0:
        return pd.DataFrame()

    if keep_first_only is not None:
        raise DeprecationWarning("""keep_first_only is deprecated since v0.3. 
        Conversion is automatic and can be turned off using the auto_cardinality option.""")

    logger.debug("Type of first element: {}".format(type(gremlin_traversal[0])))

    if type(gremlin_traversal[0]) is dict:
        if flatten_dict:
            gremlin_traversal = [_flatten(_, sep='.') for _ in gremlin_traversal]
        if key_value_pairs:
            df = pd.DataFrame(data={"value": [list(_.values())[0] for _ in gremlin_traversal]},
                              index=[list(_.keys())[0] for _ in gremlin_traversal])
        else:
            df = pd.DataFrame(gremlin_traversal)
    elif isinstance(gremlin_traversal[0], Element):
        df = pd.DataFrame([_.__dict__ for _ in gremlin_traversal])
    elif type(gremlin_traversal[0]) is Path:
        df = pd.DataFrame([dict(enumerate(_)) for _ in gremlin_traversal])
    else:
        df = pd.DataFrame(gremlin_traversal)
    if auto_cardinality:
        return df.applymap(_get_singular)
    else:
        return df