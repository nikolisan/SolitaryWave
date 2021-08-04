import vtk
import paraview
import os

def get_vtks(dirname):
    for filename in os.listdir(dirname):
        if filename.startswith('PartFluid_'):
            yield filename

def open_vtk(f):
    r = vtk.vtkDataSetReader()
    r.SetFileName(f)
    r.Update()
    data = r.GetOutput()
    return data

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


if __name__ == '__main__':
    new_dir = os.path.join(os.getcwd(),'test')
    dirname = os.path.join(os.getcwd(),'KdV\CaseSolitaryWallS2_out\particles')
    for f in get_vtks(dirname):
        print('Processing: ', f)
        save_ = os.path.join(new_dir, f)
        data = open_vtk(os.path.join(dirname, f)) 
        write_vtk(data, save_)