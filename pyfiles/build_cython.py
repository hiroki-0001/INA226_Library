#!/usr/bin/env python3

from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

extensions = [
    Extension("cython_logging_volt_current_twin", ["logging_volt_current_twin.pyx"])
]

setup(
    ext_modules=cythonize(extensions,
                          compiler_directives={
                             "language_level": 3,
                             "boundscheck": False,
                             "initializedcheck": False,
                             "cdivision": True,
                             "infer_types": True
                         })
)
