"""Explicitly import the scripts module.

See Also:
    https://www.kennethreitz.org/essays/repository-structure-and-python
"""
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

import scripts
