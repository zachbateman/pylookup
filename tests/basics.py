import unittest
import sys
sys.path.insert(1, '..')
import pylookup
import pandas


class TestLookup(unittest.TestCase):

    def add_matched_column(self):
        main = pandas.read_csv('main_table.csv')
        reference = pandas.read_csv('reference_table.csv')

        pylookup('TYPE', main, reference)

        self.assertTrue(...)




if __name__ == '__main__':
    unittest.main(buffer=True)
