from vtk.util import numpy_support as VN
from tqdm import tqdm
import pandas as pd
import vtk
import os


def get_number_of_vtks(dirname):
    count = 0
    for filename in os.listdir(dirname):
        if filename.startswith('PartFluid_'):
            count += 1
    return count

def get_vtks(dirname):
    for filename in os.listdir(dirname):
        if filename.startswith('PartFluid_'):
            yield filename

def get_vtks_list(dirname):
    vlist = []
    for v in get_vtks(dirname):
        vlist.append(v)
    return vlist

def open_vtk(f):
    r = vtk.vtkDataSetReader()
    r.SetFileName(f)
    r.ReadAllVectorsOn()
    r.ReadAllScalarsOn()
    r.Update()
    polydata = r.GetOutput()
    return polydata

def write_vtk(data, f):
    try:
        w = vtk.vtkDataSetWriter()
        w.SetInputData(data)
        w.SetFileName(f)
        w.Write()
    except Exception as e:
        print(e)
    finally:
        return True

def get_points_coords(polydata):
    coords_array = VN.vtk_to_numpy(polydata.GetPoints().GetData())
    return coords_array

def get_array(polydata, name):
    return VN.vtk_to_numpy(polydata.GetPointData().GetArray(name))

def get_array_names(polydata):
    pointdata = polydata.GetPointData()
    return [pointdata.GetArrayName(i) for i in range(pointdata.GetNumberOfArrays())]

def numpy_to_df(array, columns):
    return pd.DataFrame(array, columns=columns)

def combine_df(*dfs):
    c = pd.concat(dfs, axis=1, join='inner')
    return c

def get_maximum_runup(dirname):
    max_z = []
    nfiles = get_number_of_vtks(dirname)
    with tqdm(total=nfiles) as pbar:
        for f in get_vtks(dirname):
            polydata = open_vtk(os.path.join(dirname, f))
            coords_array = get_points_coords(polydata)
            coords = numpy_to_df(coords_array, ['x', 'y', 'z'])
            max_z.append(max(coords.z))
            pbar.update(1)
    max_runup = max(max_z)
    ind = max_z.index(max_runup)
    return max_runup, ind


if __name__ == '__main__':
    import argparse    
   
    parser = argparse.ArgumentParser(description='Extracts the maximum runup value for a given simulation')
    parser.add_argument('-c', '--case', dest='case', required=True,metavar='CASE', help='Case name')
    parser.add_argument('-m', '--method', dest='method', required=False, metavar='METHOD', help='Wave generation method')
    args = parser.parse_args()
    case = args.case + '_out'
    method = args.method
    if method is not None:
        dirname = os.path.join(os.getcwd(), method + '\\' + case + '\particles')
    else:
        dirname = os.path.join(os.getcwd(), case + '\particles')
    
    max_runup, ind = get_maximum_runup(dirname)
    print('Maximum runup in: ', ind, ' : ', max_runup)