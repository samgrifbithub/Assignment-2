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
    electricity_and_heat_co2_emissions: float
    electricity_and_heat_co2_emissions_per_capita: float
    energy_co2_emissions: float
    energy_co2_emissions_per_capita:float
    total_co2_emissions_excluding_lucf: float
    total_co2_emissions_excluding_lucf_per_capita:float

LinkedList: TypeAlias = Optional['RLNode']

@dataclass(frozen=True)
class RLNode:
    first: Row
    rest: LinkedList

#represents string as float
def is_float(val: str) -> Optional[float]:
    if val == "":
        return None
    else:
        return float(val)
    
#converts an array to a row
def array_to_row(array: List[str]) -> Row:
    return Row(
        array[0], 
        int(array[1]),
        is_float(array[2]), 
        is_float(array[3]),
        is_float(array[4]),
        is_float(array[5]),
        is_float(array[6]),
        is_float(array[7]),
    )

#reads a csv lines and returns a linked list
def read_csv_lines (filename: str) -> LinkedList:
    expected_labels : List[str] = ['country',
        'year',
        'electricity_and_heat_co2_emissions',
        'electricity_and_heat_co2_emissions_per_capita',
        'energy_co2_emissions',
        'energy_co2_emissions_per_capita',
        'total_co2_emissions_excluding_lucf',
        'total_co2_emissions_excluding_lucf_per_capita',
    ]
    with open(filename, newline="") as csvfile:
        iter = csv.reader(csvfile)
        topline : List[str] = next(iter)
        if not (topline == expected_labels):
            raise ValueError(f"unexpected first line: got: {topline}")
        result : LinkedList = None
        for line in iter:
            result = RLNode(array_to_row(line), result)
    return result

#returns # of nodes in linkedlist
def listlen(lst: LinkedList) -> int:
    match lst:
        case None:
            return 0
        case RLNode(_,rest):
            return 1+ listlen(rest)

Check = Literal["less_than", "equal", "greater_than"]

#the functions verifies domain comparison to a given value
def verify(row: Row, domain: str, check: Check, value: Any) -> bool:
    domain = getattr(row, domain)
    if domain is None:
         return False
    if check == 'less than':
         return domain < value
    elif check == 'equal':
         return domain == value
    elif check == "greater_than":
         return domain > value
    else:
         raise ValueError("Incorrect Check")

#filters a linkedlist based on check
def filter(lst: LinkedList, domain: str, check: Check, value:Any) -> LinkedList:
     if lst is None:
        return None
     filtered = filter(lst.rest, domain, check, value)
     if verify(lst.first, domain, check, value):
          return RLNode(lst.first, filtered)
     else:
        return filtered
     
#counts # of countries 
def answer_1(lst:LinkedList)-> int:
     return listlen(lst)//30

#finds all the Mexican Rows
def answer_2(lst:LinkedList) -> LinkedList:
    return filter(lst, 'country', 'equal', "Mexico")

#finds all the rows higher than american's in 1990
def answer_3(lst: LinkedList) -> LinkedList:
    us_1990 = filter(lst, "country", "equal", "United States")
    us_1990 = filter(us_1990, "year", "equal", 1990)
    us_per_capita = us_1990.first.total_co2_emissions_excluding_lucf_per_capita
    return filter(lst, "total_co2_emissions_excluding_lucf_per_capita", "greater_than", us_per_capita)

#finds all the rows higher than american's in 2020
def answer_4(lst: LinkedList) -> LinkedList:
    us_2020 = filter(lst, "country", "equal", "United States")
    us_2020 = filter(us_2020, "year", "equal", 2020)
    us_per_capita = us_2020.first.total_co2_emissions_excluding_lucf_per_capita
    return filter(lst, "total_co2_emissions_excluding_lucf_per_capita", "greater_than", us_per_capita)

#finds population of some bum ass town named luxemboureg in 2014
def answer_5(lst: LinkedList) -> float:
    lux = filter(lst, "country", "equal", "Luxembourg")
    lux = filter(lux, "year", "equal", 2014)
    return lux.first.total_co2_emissions_excluding_lucf / lux.first.total_co2_emissions_excluding_lucf_per_capita

#finds chinese gas emissions from 1990 to 2020
def answer_6(lst: LinkedList) -> float:
    china_1990 = filter(lst, "country", "equal", "China")
    china_1990 = filter(china_1990, "year", "equal", 1990)
    china_2020 = filter(lst, "country", "equal", "China")
    china_2020 = filter(china_2020, "year", "equal", 2020)
    return china_2020.first.electricity_and_heat_co2_emissions / china_1990.first.electricity_and_heat_co2_emissions

#predict china emissions in 2070
def answer_7(lst: LinkedList) -> float:
    china_2020 = filter(lst, "country", "equal", "China")
    china_2020 = filter(china_2020, "year", "equal", 2020)
    multiplier = answer_6(lst)
    return china_2020.first.electricity_and_heat_co2_emissions * (multiplier ** 50)

class Tests(unittest.TestCase):
    def test_listlen(self):
        row1 = Row("Lithuania", 1994, 7.27, 1.9281462, 14.44, 3.8297703, 14.82, 3.930554)
        row2 = Row("Lithuania", 1995, 6.41, 1.710579, 13.44, 3.586612, 13.75, 3.669339)
        lst = RLNode(row1, RLNode(row2, None))
        self.assertEqual(listlen(lst), 2)
        self.assertEqual(listlen(None), 0)

    def test_filter(self):
        row1 = Row("Lithuania", 1994, 7.27, 1.9281462, 14.44, 3.8297703, 14.82, 3.930554)
        row2 = Row("Lithuania", 1995, 6.41, 1.710579, 13.44, 3.586612, 13.75, 3.669339)
        lst = RLNode(row1, RLNode(row2, None))
        result = filter(lst, "year", "equal", 1994)
        self.assertEqual(result.first.year, 1994)
        self.assertIsNone(result.rest)

    def test_verify(self):
        row = Row("Lithuania", 1994, 7.27, 1.9281462, 14.44, 3.8297703, 14.82, 3.930554)
        self.assertTrue(verify(row, "country", "equal", "Lithuania"))
        self.assertTrue(verify(row, "year", "greater_than", 1990))

    def test_array_to_row(self):
        array = ["Lithuania", "1994", "7.27", "1.9281462", "14.44", "3.8297703", "14.82", "3.930554"]
        row = array_to_row(array)
        self.assertEqual(row.country, "Lithuania")
        self.assertEqual(row.year, 1994)

    def test_read_csv_lines(self):
        result = read_csv_lines("sample-file.csv")
        self.assertTrue(result is not None)
        self.assertEqual(result.first.country, "Lithuania")
if (__name__ == '__main__'):
    unittest.main()
