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
        #Add enrichment only to atom percent definitions
        if 'enrichment' in readfile.columns:
            #store enrichmetn indexes
            enr_idx = [index for index,i in enumerate(df["enrichment"]) if not np.isnan(i)]
        else:
            enr_idx = []

        if 'ao' in readfile.columns:
            mat = openmc.Material(
                            temperature=readfile['Temperature'][0])
            mat.set_density('g/cm3',readfile["Density"][0])
            for index,raw in readfile.iterrows():

                if index in enr_idx:

                    if raw["Element"][-1].isnumeric():
                        mat.add_nuclide(raw["Element"],raw["ao"],enrichment=raw["enrichment"])
                    else:
                        mat.add_element(raw["Element"],raw["ao"],enrichment=raw["enrichment"])
                else:

                    if raw["Element"][-1].isnumeric():
                        mat.add_nuclide(raw["Element"],raw["ao"])
                    else:
                        mat.add_element(raw["Element"],raw["ao"])


        elif 'wo' in readfile.columns:
            mix_mat = []
            for index,raw in readfile.iterrows():
                _mat = openmc.Material(name=raw["Element"],
                                temperature=readfile['Temperature'][0])
                _mat.set_density('g/cm3',readfile["Density"][0])

                if raw["Element"][-1].isnumeric():
                    _mat.add_nuclide(raw["Element"],1)
                else:
                    _mat.add_element(raw["Element"],1)
                mix_mat.append(_mat)
            mat = openmc.Material.mix_materials(mix_mat,
                                        [i for i in readfile['wo']],
                                        'wo')
        else:
            msg = (
                f'Not valid column name for file {namefile}'
                f'column names {readfile.columns} is neither "ao" nor "wo"')
            raise ValueError(msg)

        if 's_alpha_beta' in readfile.columns:
            mat.add_s_alpha_beta(readfile['s_alpha_beta'][0])
        else:
            pass

        if 'dagmc_name' in readfile.columns:
            mat.name = readfile['dagmc_name'][0]
        else:
            mat.name = namefile.split(".")[0]
        _mats.append(mat)
    return _mats
