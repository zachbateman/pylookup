'''
PyLookup module designed for simple, intelligent matching and populating between two tables.
'''
from typing import Union
from rapidfuzz import process
import pandas
from statistics import mean
from collections import defaultdict
import copy
import click



def pylookup(column_to_fill: str, main_table, reference_table, *args, force_name: bool=False, main_cols_for_matching=None, inplace=False, **kwargs) -> Union[None, pandas.DataFrame]:
    '''
    Main function that handles filling a column of the "main_table" arg
    based on data matched from the "reference_table" arg.

    Returns modified "main_table" by default.
    Can specify inplace=True to modify main_table in place instead of returning a modified copy.

    For initial development, assuming tables are provided as Pandas DataFrames.
    Ideally extend to other non-pandas data formats in the future.
    '''
    # check if column is in main
    closest_column = column_check(column_to_fill, main_table) if not force_name else column_to_fill

    # check for reference columns that can link with other columns in main
    main_col_matches = matchable_columns(main_table, reference_table, main_cols_for_matching)

    print('Populating column...')
    # pre-loaded dictionary of sets for reference columns avoids .tolist() more than once
    reference_column_values = {ref_col: [str(x) for x in reference_table[ref_col].tolist()] for ref_col in reference_table.columns}
    # iterate over main and set value of column_to_fill based on best match from reference
    new_values = []
    for i, row in main_table.iterrows():
        match_row_counts = defaultdict(int)
        for main_col, match_ref_columns in main_col_matches.items():
            main_val = row[main_col]
            for ref_col in match_ref_columns:
                ref_vals = reference_column_values[ref_col]

                for i, val in enumerate(ref_vals):
                    if val in main_val:
                        match_row_counts[i] += 0.1

                try:
                    closest_matches = [t for t in process.extract(main_val, ref_vals, limit=3) if t[1] > 50]
                    closest_match_scores = {t[0]: t[1] for t in closest_matches}
                    # loop adds 1 if score is 50 and 2 if score is 100 with a linear scale in between
                    for index, val in [(i, val) for i, val in enumerate(ref_vals) if val in set(t[0] for t in closest_matches)]:
                        match_row_counts[index] += closest_match_scores[val] / 50
                except TypeError:
                    closest_matches = []

        # now that best row counts are determined, assign best possible matched value
        if len(match_row_counts) > 0:
            max_count = max(match_row_counts.values())
            match_indexes = sorted(set(i for i, count in match_row_counts.items() if count == max_count))
        else:
            match_indexes = []

        if len(match_indexes) == 1:
            match_index = match_indexes[0]
            match_val = reference_table.iloc[match_index][column_to_fill]
        elif len(match_indexes) > 1:
            match_vals = [reference_table.iloc[match_index][column_to_fill] for match_index in match_indexes]
            if len(set(match_vals)) > 1:
                print('Unable to find explicit match... picking first option.')
            match_val = match_vals[0]
        else:
            match_val = None
        new_values.append(match_val)

    column = closest_column if closest_column else column_to_fill
    if inplace:
        main_table[column] = new_values
        print(f'main_table now has updated column {column}')
    else:
        new_main = copy.deepcopy(main_table)
        new_main[column] = new_values
        return new_main



def column_check(column, table) -> str:
    '''
    Check for column or close match in table.
    Return empty string if no valid match.
    '''
    if column in table.columns:
        return column

    closest = process.extract(column, table.columns, limit=1)[0]
    if closest[1] > 90:
        print(f'Column {column} matched to {closest[0]}')
        return closest[0]
    else:
        return ''


def matchable_columns(main_table, reference_table, main_cols_for_matching) -> dict:
    '''
    Determine which ref columns can help tie to each main column (if possible).
    '''
    if not main_cols_for_matching:
        main_cols_for_matching = set(main_table.columns)
    # pre-loaded dictionary of sets for reference columns avoids .tolist() more than once
    # set allows for fast check of exact match and works with process.extract
    reference_column_values = {ref_col: set(str(x) for x in reference_table[ref_col].tolist()) for ref_col in reference_table.columns}
    main_col_matches = defaultdict(list)
    if len(main_table) > 30:
        main_sample = main_table.sample(n=30, random_state=1)  # random state for reproducibility
    else:
        main_sample = main_table
    for main_col in [col for col in main_table.columns if col in main_cols_for_matching]:
        main_vals = [str(x) for x in main_sample[main_col].tolist()]
        for ref_col in reference_table.columns:
            ref_vals = reference_column_values[ref_col]
            scores = []
            for main_val in main_vals:  # sampled above to improve speed
                if main_val in ref_vals:  # early exit if a perfect match is in ref_vals
                    main_col_matches[main_col].append(ref_col)
                    break
                try:
                    score = process.extract(main_val, ref_vals, limit=1)[0][1]
                except TypeError:
                    score = 0
                scores = sorted((score, *scores), reverse=True)
                if score > 97 or mean(scores[:3]) > 85:  # exit as soon as a good or reasonably good matches are found
                    main_col_matches[main_col].append(ref_col)
                    break
    if not main_col_matches:
        print('No reference columns were found suitable for matching!')
    return main_col_matches


@click.command()
@click.argument('column_to_fill')
@click.argument('main_file')
@click.argument('reference_file')
def file_lookup(column_to_fill, main_file, reference_file) -> None:

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


    pylookup(column_to_fill, main_df, ref_df, inplace=True)

    if '.xl' in main_file:
        main_df.to_excel(main_file, index=False)
    elif '.csv' in main_file:
        main_df.to_csv(main_file, index=False)
    print(f'Saved updated {main_file}.')
