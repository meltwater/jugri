
# JUGRI

![PyPI - Downloads](https://img.shields.io/pypi/dm/jugri.svg)
![Travis (.org)](https://img.shields.io/travis/meltwater/jugri.svg)


The JUpyter-GRemlin Interface. 
The Gremlinpython package is easy to use to 
create queries against any property graph 
that supports the Tinkerpop interface.
However, parsing the gremlin results is more complex 
as the returned list can contain many objects.
The JUGRI package will help the developer by providing 
an easy to use interface to convert these results into 
the widely used Pandas DataFrame. 

More features are on their way...

[![JUGRI Logo](https://underthehood.meltwater.com/images/own/2018-12-14-jugri-the-jupyter-gremlin-interface/jupyter-gremlin-logo.png)](https://www.travis-ci.org/meltwater/jugri)

## Requirements

Tested on Python 3.7
- `gremlinpython`
- `pandas`

## Install/update

### Install from PyPI (the usual way)

```
pip install --user --upgrade jugri
```

### Install from source

```
pip install --user --upgrade -e git+git@github.com:meltwater/jugri.git#egg=jugri
```

or (using https)

```
pip install --user --upgrade -e git+https://github.com/meltwater/jugri.git#egg=jugri
```

## Usage

Convert Gremlin query results to a Pandas DataFrame:

```python
import jugri
from gremlin_python.structure.graph import Graph

graph = Graph()
g = graph.traversal()

df = jugri.to_df(g.V().valueMap(True).limit(10))

# df is a Pandas DataFrame with the results of the query.
```

You can find a [Jupyter notebook example](https://github.com/meltwater/jugri/blob/master/example/Pandification.ipynb)
in the [`example`](example) folder.

## Uninstall

```
pip uninstall jugri
```
