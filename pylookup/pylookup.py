'''
PyLookup module designed for simple, intelligent matching and populating between two tables.
'''
import fuzzywuzzy
import pandas



def pylookup(column_to_fill: str, main_table, reference_table, *args, **kwargs) -> None:
    '''
    Main function that handles filling a column of the "main_table" arg
    based on data matched from the "reference_table" arg.

    For initial development, assuming tables are provided as dataframes.
    Ideally extend to other non-pandas data formats in the future.
    '''
    pass
