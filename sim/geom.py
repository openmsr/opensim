import os, sys
import openmc
import openmc.lib
import os
import getopt, sys


class define_geom:

    def __init__(self,h5mfilename,planes,coredim):
        self.h5mfilename = h5mfilename
        self.planes = planes
        self.coredim = coredim

    def create_xml(self):
        dag_univ = openmc.DAGMCUniverse(str(self.h5mfilename))
        geom = openmc.Geometry(root=dag_univ)
        geom.export_to_xml()
        return geom

    def plot_geom(self,mats):
        plots = []
        for plane in self.planes:
            plot = openmc.Plot()
            plot.origin = tuple([(self.coredim[0] + self.coredim[3]) / 2,
                                 (self.coredim[1] + self.coredim[4]) / 2,
                                 (self.coredim[2] + self.coredim[5]) / 2])
            plot.color_by = 'material'
            if plane == 'vox':
                plot.type = 'voxel'
                plot.width = tuple([(abs(self.coredim[0])
                                    + abs(self.coredim[3])),
                                    (abs(self.coredim[1])
                                    + abs(self.coredim[4])),
                                    (abs(self.coredim[2])
                                    + abs(self.coredim[5]))])
                plot.pixels = tuple([int((abs(self.coredim[0])
                                    + abs(self.coredim[3])) * 5),
                                     int((abs(self.coredim[1])
                                    + abs(self.coredim[4])) * 5),
                                     int((abs(self.coredim[2])
                                    + abs(self.coredim[5])) * 5)])
            elif plane == 'xy':
                plot.basis = plane
                plot.width = tuple([(abs(self.coredim[0])
                                    + abs(self.coredim[3])),
                                    (abs(self.coredim[1])
                                    + abs(self.coredim[4]))])
                plot.pixels = tuple([int((abs(self.coredim[0])
                                    + abs(self.coredim[3])) * 5),
                                     int((abs(self.coredim[1])
                                    + abs(self.coredim[4])) * 5)])
            elif plane == 'yz':
                plot.basis = plane
                plot.width = tuple([(abs(self.coredim[1])
                                    + abs(self.coredim[4])),
                                    (abs(self.coredim[2])
                                    + abs(self.coredim[5]))])
                plot.pixels = tuple([int((abs(self.coredim[1])
                                    + abs(self.coredim[4])) * 5),
                                     int((abs(self.coredim[2])
                                    + abs(self.coredim[5])) * 5)])
            elif plane == 'xz':
                plot.basis = plane
                plot.width = tuple([(abs(self.coredim[0])
                                    + abs(self.coredim[3])),
                                    (abs(self.coredim[2])
                                    + abs(self.coredim[5]))])
                plot.pixels = tuple([int((abs(self.coredim[0])
                                    + abs(self.coredim[3])) * 5),
                                     int((abs(self.coredim[2])
                                    + abs(self.coredim[5])) * 5)])
            else:
                continue
            plots.append(plot)
        Plots = openmc.Plots(plots)
        Plots.export_to_xml()
        openmc.plot_geometry()
