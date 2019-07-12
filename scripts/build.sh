#!/usr/bin/env bash

python setup.py clean --quiet
python setup.py cython --quiet
python setup.py sdist bdist_wheel

python3 setup.py clean --quiet
python3 setup.py cython --quiet
python3 setup.py sdist bdist_wheel
