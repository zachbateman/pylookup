'''
Command Line Interface for PyLookup.
'''
from pylookup import pylookup
import pandas
import click


@click.command()
@click.argument('column_to_fill')
@click.argument('main_file')
@click.argument('reference_file')
def file_lookup(column_to_fill, main_file, reference_file):

    if '.xl' in main_file:
        main_df = pandas.read_excel(main_file)
    elif '.csv' in main_file:
        main_df = pandas.read_csv(main_file)
    else:
        print('Error!  Main file must be .csv or .xlsx!')

    if '.xl' in reference_file:
        ref_df = pandas.read_excel(reference_file)
    elif '.csv' in reference_file:
        ref_df = pandas.read_csv(reference_file)
    else:
        print('Error!  Reference file must be .csv or .xlsx!')


    pylookup(column_to_fill, main_df, ref_df)

    if '.xl' in main_file:
        main_df.to_excel(main_file, index=False)
    elif '.csv' in main_file:
        main_df.to_csv(main_file, index=False)
    print(f'Saved updated {main_file}.')



if __name__ == '__main__':
    file_lookup()
