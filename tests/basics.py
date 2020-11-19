import unittest
import sys
sys.path.insert(1, '..')
import pylookup
import pandas


class TestLookup(unittest.TestCase):

    def test_add_matched_column(self):
        main = pandas.read_csv('main_table.csv')
        reference = pandas.read_csv('reference_table.csv')

        print(main)
        pylookup.pylookup('TYPE', main, reference)
        pylookup.pylookup('ANIMAL2', main, reference, force_name=True)
        print(main)

        self.assertTrue('TYPE' in main.columns and 'ANIMAL2' in main.columns)




if __name__ == '__main__':
    unittest.main(buffer=False)
