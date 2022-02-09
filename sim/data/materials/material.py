import numpy as np
import pandas as pd
import openmc
import os, sys
from pathlib import Path


def read_csv_material_files(material_data):

    #check for default library, else use provided path
    path =  Path(__file__).parent
    if material_data in os.listdir(path):
        path =  Path(__file__).parent / material_data
    else:
        path = material_data

    #get csv files
    _files = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            _files.append((file,pd.read_csv(path/file)))
    return _files

def make_openmc_material(readfiles):
    _mats = []
    for namefile,readfile in readfiles:

        if readfile.columns[2] == 'ao':
            mat = openmc.Material(
                            temperature=readfile['Temperature'].mean())
            for index,raw in readfile.iterrows():
                mat.set_density('g/cm3',raw["Density"])
                if raw["Element"][-1].isnumeric():
                    mat.add_nuclide(raw["Element"],raw["ao"])
                else:
                    mat.add_element(raw["Element"],raw["ao"])

        elif readfile.columns[2] == 'wo':
            mix_mat = []
            for index,raw in readfile.iterrows():
                mat = openmc.Material(name=raw["Element"],
                                temperature=readfile['Temperature'].mean()
                                )
                mat.set_density('g/cm3',raw["Density"])

                if raw["Element"][-1].isnumeric():
                    mat.add_nuclide(raw["Element"],1)
                else:
                    mat.add_element(raw["Element"],1)
                mix_mat.append(mat)
            mat = openmc.Material.mix_materials(mix_mat,
                                        [i for i in readfile['wo']],
                                        'wo')
        else:
            msg = (
                f'Not valid column name for file {namefile}'
                f'column name {readfile.columns[2]} is neither "ao" nor "wo"')
            raise ValueError(msg)

        if 's_alpha_beta' in readfile.columns:
            mat.add_s_alpha_beta(readfile['s_alpha_beta'][0])
        else:
            pass
        mat.name = namefile.split(".")[0]
        _mats.append(mat)
    return _mats
