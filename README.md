# PyLookup

PyLookup is a fuzzy-matching, auto-table-updating library and command-line tool inspired by the "VLOOKUP" function in Excel.


# Installation

```
pip install pylookup
```

# Command Line Interface Usage

 - To add and populate the "COLUMN" column in "excel_to_populate" from the data in "excel_with_column",
 simple run the following command.  This currently works for .xlsx (Excel) files and .csv files.

```
pylookup COLUMN excel_to_populate.xlsx excel_with_column.xlsx
```



License
----
MIT
