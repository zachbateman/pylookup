'''
PyLookup module designed for simple, intelligent matching and populating between two tables.
'''
from fuzzywuzzy import fuzz, process
import pandas
from statistics import mean
from collections import defaultdict
from pprint import pprint as pp



def pylookup(column_to_fill: str, main_table, reference_table, *args, force_name: bool=False, **kwargs) -> None:
    '''
    Main function that handles filling a column of the "main_table" arg
    based on data matched from the "reference_table" arg.
    Modifies "main_table" in place.

    For initial development, assuming tables are provided as dataframes.
    Ideally extend to other non-pandas data formats in the future.
    '''

    # check if column is in main
    if not force_name:
        closest_column = column_check(column_to_fill, main_table)
    else:
        closest_column = column_to_fill

    # check for reference columns that can link with other columns in main
    main_match_cols = set(col for col in main_table.columns) # if col != closest_column)
    main_col_matches = defaultdict(list)

    for main_col in main_match_cols:
        main_vals = main_table[main_col].tolist()
        for ref_col in reference_table.columns:
            ref_vals = [str(x) for x in reference_table[ref_col].tolist()]

            best_match_scores = sorted([process.extract(str(main_val), ref_vals, limit=1)[0][1] for main_val in main_vals], reverse=True)
            if mean(best_match_scores[:3]) > 90:
                main_col_matches[main_col].append(ref_col)
    pp(main_col_matches)
    if not main_col_matches:
        print('No reference columns were found suitable for matching!')
    pp(main_col_matches)

    # iterate over main and set value of column_to_fill based on best match from reference
    new_values = []
    for i, row in main_table.iterrows():
        match_row_counts = {r: 0.0 for r in range(len(reference_table))}
        for main_col, match_ref_columns in main_col_matches.items():
            main_val = row[main_col]
            for ref_col in match_ref_columns:
                ref_vals = reference_table[ref_col].tolist()
                closest_matches = [t for t in process.extract(main_val, ref_vals, limit=3) if t[1] > 80]

                for index in [i for i, val in enumerate(ref_vals) if val in [t[0] for t in closest_matches]]:
                    match_row_counts[index] += 1

                if len(closest_matches) > 1 and closest_matches[0][1] - closest_matches[1][1] > 5 and closest_matches[0][1] > 95:
                    for index in [i for i, val in enumerate(ref_vals) if val == closest_matches[0][0]]:
                        match_row_counts[index] += 1

        # pp(match_row_counts)
        max_count = max(match_row_counts.values())
        match_indexes = sorted(set(i for i, count in match_row_counts.items() if count == max_count))
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

    print(new_values)
    main_table[closest_column if closest_column else column_to_fill] = new_values



def column_check(column, table) -> str:
    '''
    Check for column or close match in table.
    Return empty string if no valid match.
    '''
    if column in table.columns:
        return column

    closest = process.extract(column, table.columns, limit=1)[0]
    print(closest)
    if closest[1] > 90:
        print(f'Column {column} matched to {closest[0]}')
        return closest[0]
    else:
        return ''
