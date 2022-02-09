import openmc
import openmc.lib
import os
import sys
import pandas as pd
from .data.materials.material import read_csv_material_files, make_openmc_material

class define_mat:

    def __init__(self,material_data):
        self.material_data = material_data

    def create_material_xml(self):
        default_mats = ['msre','are','onion','calandria','zpre']

        # create xml files from default libs
        if self.material_data in default_mats:
            readmat = read_csv_material_files(self.material_data)
            mats = openmc.Materials([mat for mat in make_openmc_material(readmat)])

        # read materials in provided directory, preference to xml files
        else:
            filenames = os.listdir(self.material_data)

            if not filenames:
                msg = (f'{self.material_data} is an empty directory')
                raise ValueError(msg)

            # sort by type
            csv_files = [os.path.splitext(f)[0] for f in filenames if f.endswith('.csv')]
            xml_files = [os.path.splitext(f)[0] for f in filenames if f.endswith('.xml')]

            # if all are .csv files
            if not xml_files:
                if not csv_files:
                    msg = (f'material files must be .csv or .xml')
                    raise FileNotFoundError(msg)
                else:
                    _files = [(f,pd.read_csv(f)) for f in filenames]
                    mats = openmc.Materials([mat for mat in make_openmc_material(_files)])

            # if all are .xml files
            elif not csv_files:
                if not xml_files:
                    msg = (f'material files must be .csv or .xml')
                    raise FileNotFoundError(msg)
                else:
                    mats = openmc.Materials()
                    for f in filenames:
                        new_mat = openmc.Materials()
                        new_mat.from_xml(f)
                        new_mat = new_mat[0]
                        mats.append(new_mat)

            # if both, prefer xml
            else:
                mats = openmc.Materials()
                for f in filenames:
                    size = len(f)
                    raw = f[:size-4]
                    if raw in xml_files:
                        new_mat = openmc.Materials()
                        new_mat.from_xml(f)
                        new_mat = new_mat[0]
                        mats.append(new_mat)
                    elif raw in csv_files:
                        _file = [(f,pd.read_csv(f))]
                        mats.append(openmc.Materials(make_openmc_material(_file))[0])
                    else:
                        msg = (f'material files must be .csv or .xml')
                        raise FileNotFoundError(msg)

        mats.export_to_xml
        return mats
