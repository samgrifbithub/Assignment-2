import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class Row:
    country: str
    year: int
    emission_type: str
    emissions: float

@dataclass(frozen=True)
class RLNode:
    first: Row
    rest: Optional['RLNode']


class Tests(unittest.TestCase):
pass
if (__name__ == '__main__'):
unittest.main()
