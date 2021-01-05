
import sys
sys.path.insert(1, '..')
import pylookup
import pandas
import cProfile


def performance_test():
    main = pandas.read_csv('main_table.csv')
    reference = pandas.read_csv('reference_table.csv')

    print(main)
    main = pylookup.pylookup('TYPE', main, reference)
    main = pylookup.pylookup('ANIMAL2', main, reference, force_name=True)

    for _ in range(30):
        main = pylookup.pylookup('TYPE', main, reference)
    print(main)



if __name__ == '__main__':
    cProfile.run('performance_test()', 'prof.prof')
