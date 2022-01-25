import openmc
import openmc.lib
import sys
from .scripts.h5m_cell_id import get_h5m_volumes

class define_tally:

    def __init__(self,h5mfilename,planes,meshsize,
                 coredim,meshscores,particle,detmat,reacmat):
        self.h5mfilename = h5mfilename
        self.planes = planes
        self.meshsize = meshsize #not IMPLEMENTED yet
        self.coredim = coredim
        self.meshscores = meshscores
        self.particle = particle
        self.detmat = detmat
        self.reacmat = reacmat

    def create_tally(self):
        return openmc.Tallies()

    def export_tally(self,tallies):
        tallies.export_to_xml()
        return tallies

    def create_keff_tally(self,tallies):
        fiss_rate = openmc.Tally(name='fiss_rate')
        abs_rate = openmc.Tally(name='abs_rate')
        fiss_rate.scores = ['nu-fission']
        abs_rate.scores = ['absorption']
        tallies.append(fiss_rate)
        tallies.append(abs_rate)
        return tallies

    def create_leak_tally(self,tallies):
        mesh = openmc.RegularMesh()
        mesh.dimension = [1, 1, 1]
        mesh.lower_left = [self.coredim[0],
                           self.coredim[1],
                           self.coredim[2]]
        mesh.width = [abs(self.coredim[0]) + abs(self.coredim[3]),
                      abs(self.coredim[1]) + abs(self.coredim[4]),
                      abs(self.coredim[2]) + abs(self.coredim[5])]
        mesh_filter = openmc.MeshSurfaceFilter(mesh)
        leak = openmc.Tally(name='leakage')
        leak.filters = [mesh_filter]
        leak.scores = ['current']
        tallies.append(leak)
        return tallies

    def create_strenght(sp,tallies):
        tally = openmc.Tally(name="heating_total")
        tally.scores = ['heating']
        tallies.append(tally)
        return tallies

    def create_rates_tally(self,tallies,mats):
        for id in self.reacmat:
            tally = openmc.Tally(name=f"{id}_reaction_rate")
            cell_id = get_h5m_volumes([self.h5mfilename,id])
            tally.filters = [openmc.CellFilter(cell_id),
                             openmc.ParticleFilter(['neutron'])]
            _mat = [mat for mat in mats if mat.name == id][0]
            tally.scores = ['(n,gamma)','absorption','fission']
            tally.nuclides = _mat.get_nuclides()
            tallies.append(tally)
        return tallies

    def create_mesh_tally(self,tallies):
        for plane in self.planes:
            mesh = openmc.RegularMesh()

            if plane == 'xy':
                mesh.dimension = [abs(self.coredim[0]) + abs(self.coredim[3]),
                                  abs(self.coredim[1]) + abs(self.coredim[4]),
                                  1]
                mesh.lower_left = [ self.coredim[0],
                                    self.coredim[1],
                                   (self.coredim[2] + self.coredim[5]) / 2]
                mesh.upper_right = [self.coredim[3],
                                    self.coredim[4],
                                   (self.coredim[2] + self.coredim[5]) / 2 + 1]
            elif plane == 'yz':
                mesh.dimension = [1,
                                  abs(self.coredim[1]) + abs(self.coredim[4]),
                                  abs(self.coredim[2]) + abs(self.coredim[5])]

                mesh.lower_left = [( self.coredim[0] + self.coredim[3]) / 2,
                                     self.coredim[1],
                                     self.coredim[2]]
                mesh.upper_right = [(self.coredim[0] + self.coredim[3]) / 2 + 1,
                                     self.coredim[4],
                                     self.coredim[5]]
            elif plane == 'xz':
                mesh.dimension = [abs(self.coredim[0]) + abs(self.coredim[3]),
                                  1,
                                  abs(self.coredim[2]) + abs(self.coredim[5])]
                mesh.lower_left =  [self.coredim[0],
                                   (self.coredim[1] + self.coredim[4]) / 2,
                                    self.coredim[2]]
                mesh.upper_right = [self.coredim[3],
                                   (self.coredim[1] + self.coredim[4]) / 2 + 1,
                                    self.coredim[5]]
            mesh_filter = openmc.MeshFilter(mesh)
            tally = openmc.Tally(name=f'mesh_{plane}')
            tally.scores = [meshscore for meshscore in self.meshscores]
            tally.filters = [mesh_filter]
            tallies.append(tally)
        return tallies


    def create_dose_tally(self,tallies):
        cell_id = get_h5m_volumes([self.h5mfilename,self.detmat])
        mesh_filter = openmc.CellFilter(cell_id)
        for particle in self.particle:
            particle_filter = openmc.ParticleFilter([particle])
            energy, dose = openmc.data.dose_coefficients(particle,'AP')
            filter = openmc.EnergyFunctionFilter(energy, dose)
            tally = openmc.Tally(name=f'dose_{particle}')
            tally.scores = ['flux']
            tally.filters=[particle_filter,filter,mesh_filter]
            tallies.append(tally)
        return tallies
