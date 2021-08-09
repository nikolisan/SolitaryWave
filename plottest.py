from logging import info
from math import inf
import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from get_runup import *
import matplotlib.pyplot as plt

def set_vtk(counter, dirname):
    name = 'PartFluid_' + str(counter).zfill(4) + '.vtk'
    return os.path.join(dirname, name)

def update_plt(fvtk, canvas, ax):
    global velc
    try:
        ax.clear()
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 2)
        ax.autoscale(False)
        polydata = open_vtk(fvtk)
        coords = numpy_to_df(get_points_coords(polydata), ['x', 'y', 'z'])
        x, z = coords.x, coords.z
        lbl_runup.config(text=f'Current runup: {max(z)}')
        vel_arr = vel_df(polydata)[velc]
        ax.scatter(x, z, s=1, c=vel_arr, cmap='coolwarm')
        canvas.draw()
    except Exception as e:
        print(e)

def key_handling(event):
    global counter, lims, dirname
    global ax
    global canvas

    if event.keycode == 37:
        counter -= 1 if counter > lims[0] else 0
    elif event.keycode == 39:
        counter += 1 if counter < lims[1] else 0

    fvtk = set_vtk(counter, dirname)
    text = fvtk.split('\\')[-1]
    lblf.config(text=f'File: {text}')
    root.title(f'VTK Viewer: {text}')
    update_plt(fvtk, canvas, ax)

def seek_plt(ncounter):
    global ax
    global canvas
    global counter, lims
    global root

    if ncounter > lims[1]:
        ncounter = lims[1]
    elif ncounter < lims[0]:
        ncounter = lims[0]

    counter = ncounter

    fvtk = set_vtk(counter, dirname)
    text = fvtk.split('\\')[-1]
    lblf.config(text=f'File: {text}')
    root.title(f'VTK Viewer: {text}')
    update_plt(fvtk, canvas, ax)

def frame_select(e):
    vtkf = cb_framesel.get()
    seek_plt(int(vtkf.split('_')[1].split('.')[0]))

def vel_select(e):
    global velc, counter
    velc = vel_cb.get()
    seek_plt(counter)

if __name__ == '__main__':

    dirname = os.path.join(os.getcwd(),'Boussinesq','CaseSolitaryWallBS4_out','particles')
    
    lims = (0, get_number_of_vtks(dirname)-1)
    counter = lims[0]
    vtk_files = [f for f in get_vtks(dirname)]

    fvtk = set_vtk(counter, dirname)
    vtkname = fvtk.split('\\')[-1]
    velc = 'x'

    root = tk.Tk()
    root.title(f'VTK Viewer: {vtkname}')
    root.bind('<Escape>', lambda e: root.quit())
    root.bind('<Key>', key_handling)

    fig = Figure(dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 2)
    ax.autoscale(False)
    canvas = FigureCanvasTkAgg(fig, master=root)
    
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

    # sidebar = tk.Frame(master=root)
    # sidebar.pack(side=tk.RIGHT)
    information_frame = tk.Frame(master=root, pady=10)
    information_frame.pack(side=tk.TOP)
    controls_frame = tk.Frame(master=root, pady=10)
    controls_frame.pack(side=tk.BOTTOM)
    framesel = tk.Frame(master=controls_frame)
    framesel.pack()
    velselfr = tk.Frame(master=controls_frame)
    velselfr.pack()

    lblf = ttk.Label(master=information_frame, text=f'File: {vtkname}')
    lblf.pack()
    lbl_nfiles = ttk.Label(master=information_frame, text=f'Amount of files: {lims[1]+1}')
    lbl_nfiles.pack()
    lbl_mrunup = ttk.Label(master=information_frame, text=f'Maximum Runup: {get_maximum_runup(dirname)}')
    lbl_mrunup.pack()
    lbl_runup = ttk.Label(master=information_frame, text='')
    lbl_runup.pack()
    lblfr = ttk.Label(master=framesel, padding=3, text='Select frame:').pack(side=tk.LEFT)
    cb_framesel = ttk.Combobox(master=framesel)
    cb_framesel['values'] = vtk_files
    cb_framesel['state'] = 'readonly'
    cb_framesel.bind('<<ComboboxSelected>>', frame_select)
    cb_framesel.pack(side=tk.LEFT)
    lblvl = ttk.Label(master=velselfr, padding=3, text='Select vel component:').pack(side=tk.LEFT)
    vel_cb = ttk.Combobox(master=velselfr)
    vel_cb['values'] = ('x', 'y', 'z', 'magnitude')
    vel_cb['state'] = 'readonly'
    vel_cb.bind('<<ComboboxSelected>>', vel_select)
    vel_cb.pack(side=tk.LEFT)

    btnRewind = ttk.Button(master=controls_frame, text="<<", command=lambda: seek_plt(lims[0]))
    btnEnd = ttk.Button(master=controls_frame, text=">>", command=lambda: seek_plt(lims[1]))
    btnFwd = ttk.Button(master=controls_frame, text=">", command=lambda: seek_plt(counter+1))
    btnPrv = ttk.Button(master=controls_frame, text="<", command=lambda: seek_plt(counter-1))

    btnRewind.pack(side=tk.LEFT)
    btnPrv.pack(side=tk.LEFT)
    btnFwd.pack(side=tk.LEFT)
    btnEnd.pack(side=tk.LEFT)

    update_plt(fvtk, canvas, ax)

    root.mainloop()