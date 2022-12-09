#!/usr/bin/env python

import os
from io import open  # for Python 2 (identical to builtin in Python 3)

from setuptools import find_packages, setup


def pyload(name):
    ns = {}
    with open(name, encoding="utf-8") as f:
        exec(compile(f.read(), name, "exec"), ns)
    return ns


# In case it's Python 2:
try:
    execfile
except NameError:
    pass
else:

    def pyload(path):
        ns = {}
        execfile(path, ns)
        return ns


repo_root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(repo_root, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
# https://packaging.python.org/guides/making-a-pypi-friendly-readme/

ns = pyload(os.path.join(repo_root, "src", "datahike", "release.py"))
version = ns["__version__"]

# fmt: off
setup(name='datahike',
      version=version,
      description="Datahike/Python bridge.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='The Datahike development team.',
      author_email='info@lambdaforge.io',
      license='MIT',
      keywords='datahike python',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        #'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
      ],
      url='http://datahike.io',
      project_urls={
          "Source": "https://github.com/replikativ/pydatahike",
          "Tracker": "https://github.com/replikativ/pydatahike/issues",
          "Documentation": "https://cljdoc.org/d/io.replikativ/datahike/",
      },
      packages=find_packages("src"),
      package_dir={"": "src"},
      python_requires=">=3.0"
      )
