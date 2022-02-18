import os, sys
import openmc
from .geom import define_geom
from .mat import define_mat
from .tally import define_tally
from .post import make_post

class def_model:

    def __init__(self,args):
        self.args = args

    def set_mat(self):
        mat = define_mat(self.args.materialdata,
                         self.args.localdata)
        mat_xml = mat.create_material_xml()
        return mat_xml

    def set_geom(self,mat_xml):
        geom = define_geom(self.args.h5mfilename,
                           self.args.planes,
                           self.args.coredim)
        geom_xml = geom.create_xml()

        if self.args.plotgeom:
            geom.plot_geom(mat_xml)
        elif self.args.runmode == 'plot-geom':
            geom.plot_geom(mat_xml)
            sys.exit()
        else:
            pass
        return geom_xml

    def set_tally(self,mat_xml):
        tally = define_tally(self.args.h5mfilename,
                             self.args.planes,
                             self.args.meshsize,
                             self.args.coredim,
                             self.args.meshscores,
                             self.args.particle,
                             self.args.detmat,
                             self.args.reacmat)
        tallies = tally.create_tally()
        tallies = tally.create_keff_tally(tallies)
        tallies = tally.create_leak_tally(tallies)
        tallies = tally.create_strenght(tallies)

        if self.args.calcreac:
            tallies = tally.create_rates_tally(tallies,mat_xml)
        else:
            pass

        if self.args.meshscores:
            tallies = tally.create_mesh_tally(tallies)
        else:
            pass

        if self.args.calcdose:
            tallies = tally.create_dose_tally(tallies)
        else:
            pass
        tally_xml = tally.export_tally(tallies)
        return tally_xml

    def set_setting(self):
        settings = openmc.Settings()
        settings.temperature = {'method':'interpolation'}
        settings.batches = self.args.batches
        settings.inactive = self.args.inactive
        settings.particles = self.args.particles
        source_area = openmc.stats.Box([i for i in self.args.coredim][0:3],
                                       [i for i in self.args.coredim][3:6],
                                       only_fissionable = True)
        settings.source = openmc.Source(space=source_area)

        if 'photon' in self.args.particle:
            settings.photon_transport = True
        else:
            pass
        settings.export_to_xml()
        return settings

    def model_run(self,geom,mats,settings,tallies):
        model = openmc.model.Model(geom,mats,settings,tallies)
        statepoint = model.run()
        return statepoint

    def set_post(self,resfile):
        post = make_post(self.args.h5mfilename,
                         self.args.detvol,
                         self.args.coredim,
                         self.args.power)
        sp = post.get_tally(resfile)
        post.calc_keff(sp)
        strength = post.calc_strenght(sp)

        if self.args.calcreac:
            post.calc_rates(sp,strength)
        else:
            pass

        if self.args.calcdose:
            post.calc_dose(sp,strength)
        else:
            pass

        if self.args.meshscores:
            post.make_plots(sp,strength)
        else:
            pass
