import openmc
import openmc.lib
import os
import sys
import pandas as pd
from .data.materials.material import read_csv_material_files, make_openmc_material

class define_mat:

    def __init__(self,material_data,local_data):
        self.material_data = material_data
        self.local_data = local_data

    def create_material_xml(self):

        # create xml files from default libs
        if self.local_data is None:
            readmat = read_csv_material_files(self.material_data)
            mats = openmc.Materials([mat for mat in make_openmc_material(readmat)])

        # read materials in provided directory, preference to xml files
        else:
            filenames = os.listdir(self.local_data)

            if not filenames:
                msg = (f'{self.local_data} is an empty directory')
                raise Exception(msg)

        # we only want one material.xml file with all materials, otherwise confusing
            xml = [os.path.join(self.local_data,f) for f in filenames if f.endswith('.xml')]
            if len(xml) == 1:
                if not mats.from_xml(xml[0]):
                    msg = (f'{xml[0]} is not a material.xml')
                    raise Exception(msg)
                else:
                    mats = openmc.Materials()
                    mats = mats.from_xml(xml[0])
            #assuming material files are either .csv, .txt or/and .xlsx
            else:
                mats = openmc.Materials()
                for f in filenames:
                    f = os.path.join(self.local_data,f)
                    if f.endswith('.csv'):
                        _mat = [(f,pd.read_csv(f))]
                    elif f.endswith('.xlsx'):
                        _mat = [(f,pd.read_excel(f))]
                    elif f.endswith('.txt'):
                        _mat = [(f,pd.read_csv(f))]
                    else:
                        #can add other extensions later
                        continue
                    mats.append(openmc.Materials(make_openmc_material(_mat))[0])

        mats.export_to_xml()
        return mats
