from get_runup import *
import os
import csv


def create_runup_list(dir_):
    maxz = []
    for case in os.listdir(dir_):
        if '_out' in case:
            print('\n', case[0:-4])
            case_dir = os.path.join(dir_, case+'\particles')
            max_runup, ind = get_maximum_runup(case_dir)
            print('Maximum runup in: ', ind, ' : ', max_runup)
            maxz.append(max_runup)
    return maxz


if __name__ == '__main__':
    import sys

    simfolders = ['KdV', 'Boussinesq']

    try:
        maximums = {}
        for sim in simfolders:
            print('\n-------------------------------------\n',sim)
            l = create_runup_list(os.path.join(os.getcwd(), sim))
            maximums[sim] = l
    except Exception as e:
        print(e)
        sys.exit(2)

    try:
        with open(os.path.join(os.getcwd(), 'extracted_runups.csv'), 'w') as fo:
            w = csv.writer(fo, delimiter=';')
            w.writerow(maximums.keys())
            w.writerows(zip(*maximums.values()))
    except Exception as e:
        print(e)
        sys.exit(2)
    finally:
        print('\n\nExtracted data are saved!')
        sys.exit()

