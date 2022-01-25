import os, sys

import matplotlib
import openmc
import openmc.lib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import pi
from .scripts.find_tally import find_tallies_by_name

class make_post:

    def __init__(self,h5mfilename,detvol,coredim,power):
        self.h5mfilename =  h5mfilename
        self.detvol = detvol
        self.coredim = coredim
        self.power = power

    def get_tally(self,resfile):
        if openmc.StatePoint(resfile).tallies_present:
            pass
        else:
            msg = ('Tallies not present')
            raise ValueError(msg)
        return openmc.StatePoint(resfile)


    def calc_keff(self,sp):
        leak = find_tallies_by_name(
                sp,
                'leakage'
                )[0]
        leak = leak.summation(
                    filter_type=openmc.MeshSurfaceFilter,
                    remove_filter=True
                    )
        k_eff = sp.k_combined
        df = pd.DataFrame(
                data=[[k_eff.nominal_value,k_eff.std_dev],
                      [leak.mean.mean(),leak.std_dev.mean()]],
                index=['k_eff','leak'],
                columns=['mean','std_dev']
                )
        df.to_csv('k_eff_leak.csv')

    def calc_rates(self,sp,strength):
        score_list=[]
        for tally in find_tallies_by_name(sp,'reaction_rate'):
            for nuclide in tally.nuclides:
                scores = tally.get_slice(
                                nuclides=[nuclide]
                                )
                for score in scores.scores:
                    value=tally.get_slice(
                                nuclides=[nuclide],
                                scores=[score]
                                ).mean.mean()
                    value = value*strength
                    score_list.append([value,score,nuclide,tally.name])
        df=pd.DataFrame(
                data=score_list,
                columns=["mean","score","nuclide","type"]
                )
        df.to_csv('reaction_rates.csv')

    def calc_strenght(self,sp):
        heating_rate = find_tallies_by_name(
                        sp,
                        'heating_total'
                        )[0].mean.mean()
        strength = self.power/(1.602*10**(-19) * heating_rate)
        return strength

    def calc_dose(self,sp,strength):
        dose_list =[]
        particle_list=[]
        for dose_tally in find_tallies_by_name(sp,'dose'):
            particle = [tally.bins for tally in
                        dose_tally.filters if
                        tally.short_name == 'Particle'
                        ][0][0]
            particle_list.append(particle)
            dose_mean = dose_tally.mean.sum()
            dose_stddev = dose_tally.std_dev.sum()
            # convert in [mSv/h]
            dose_mean = dose_mean / self.detvol * strength \
                       * (10**(-12)) / (10**(-3)) * 3600
            dose_stddev = dose_stddev / self.detvol * strength \
                       * (10**(-12)) / (10**(-3)) * 3600
            dose_list.append([dose_mean,dose_stddev])
        df = pd.DataFrame(
                data=dose_list,
                index=particle_list,
                columns=['mean [mSv/h]','std_dev [mSv/h]']
                )
        df.to_csv('dose.csv')

    def make_plots(self,sp,strenght):
        for mesh_tally in find_tallies_by_name(sp,'mesh'):
            for score_name in mesh_tally.scores:
                score = mesh_tally.get_slice(scores=[score_name])
                data_frame = score.get_pandas_dataframe()
                values = np.array(data_frame["mean"])
                plane = score.name.split('_')[1]

                if plane == 'xy':
                    values=values.reshape([abs(self.coredim[1])
                                         + abs(self.coredim[4]),
                                           abs(self.coredim[0])
                                         + abs(self.coredim[3])]
                                         )
                    extent=(self.coredim[0],
                            self.coredim[3],
                            self.coredim[1],
                            self.coredim[4]
                            )
                elif plane == 'yz':
                    values=values.reshape([abs(self.coredim[2])
                                         + abs(self.coredim[5]),
                                           abs(self.coredim[1])
                                         + abs(self.coredim[4])]
                                         )
                    extent=(self.coredim[1],
                            self.coredim[4],
                            self.coredim[2],
                            self.coredim[5]
                            )
                elif plane == 'xz':
                    values=values.reshape([abs(self.coredim[2])
                                         + abs(self.coredim[5]),
                                           abs(self.coredim[0])
                                         + abs(self.coredim[3])]
                                         )
                    extent=(self.coredim[0],
                            self.coredim[3],
                            self.coredim[2],
                            self.coredim[5]
                            )
                fig, ax = plt.subplots()
                pos = ax.imshow(
                        values*strenght,
                        aspect='auto',
                        origin='lower',
                        extent=extent,
                        cmap='RdBu',
                        label=score_name
                        )
                cbar = plt.colorbar(pos,ax=ax)
                cbar.ax.set_ylabel(f'{score_name}', rotation=270)
                ax.set_xlabel(f'{plane[0]} [cm]')
                ax.set_ylabel(f'{plane[1]} [cm]')
                ax.set_title(f'{score_name}_{plane}')
                plt.savefig(f'{score_name}_{plane}.png',dpi=600)

    ## TO BE IMPLEMENTED
    #def create_vtk(self,tallies):
        #tally = sp.get_tally()
        #write_mesh_tally_to_vtk(tally=tally,filename='tally.vtk')
