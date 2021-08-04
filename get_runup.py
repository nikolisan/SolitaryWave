from matplotlib.pyplot import get
import vtk
from vtk.util import numpy_support as VN
from tqdm import tqdm
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
    return coords_array[:,0] , coords_array[:,1] , coords_array[:,2]

def get_array(polydata, name):
    return VN.vtk_to_numpy(polydata.GetPointData().GetArray(name))

def get_maximum_runup(dirname):
    max_z = []
    nfiles = get_number_of_vtks(dirname)
    with tqdm(total=nfiles) as pbar:
        for f in get_vtks(dirname):
            # print('Processing: ', f)
            polydata = open_vtk(os.path.join(dirname, f))
            z = get_points_coords(polydata)[2]
            max_z.append(max(z))
            pbar.update(1)

    max_runup = max(max_z)
    ind = max_z.index(max_runup)

    return max_runup, ind

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import argparse

    def plot_test(dirname):
        vlist = get_vtks_list(dirname)
        fvtk = os.path.join(dirname, vlist[100])
        # Get the data from the vtk file
        polydata = open_vtk(fvtk)
        # Get the point coordinates
        x, y, z = get_points_coords(polydata)[0], get_points_coords(polydata)[1], get_points_coords(polydata)[2]
        # Get the velocity in x direction
        vel_array = get_array(polydata, 'Vel')
        # Plot the profile
        plt.scatter(x, z)
        plt.show()


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