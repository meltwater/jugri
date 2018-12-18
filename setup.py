#!/usr/bin/env python

from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


def read_all(filename):
    """
    Read file line by line
    """
    with open(filename,"r") as myfile:
        yield myfile.readline()


dependencies = list(read_all('requirements.txt'))


setup(name='jugri',
      version='0.4.0',
      description=long_description,
      description_content_type='text/markdown',
      author='Laszlo Velinszky',
      author_email='laszlo.velinszky@meltwater.com',
      url='https://github.com/meltwater/jugri',
      license='ASL2',
      packages=find_packages(),
      setup_requires=["pytest-runner"] + dependencies,
      tests_requires=["pytest"] + dependencies,
      test_suite="tests"
)
