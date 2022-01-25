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
        readmat = read_csv_material_files(self.material_data)
        mats = openmc.Materials([mat for mat in make_openmc_material(readmat)])
        mats.export_to_xml()
        return mats
