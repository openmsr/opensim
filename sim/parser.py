import dataclasses
import os, sys
from typing import List, Any
from pathlib import Path
import argparse

def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('--h5mfilename',
                        action='store',
                        type=Path,
                        default=None,
                        help='the path to a h5m file')

    parser.add_argument('-r', '--runmode',
                        action='store',
                        choices=['run','plot-geom'],
                        default='run',
                        help='Run mode: "run" or "plot-geometry"')

    parser.add_argument('-b', '--batches',
                        action='store',
                        type=int,
                        default=100,
                        help='Number of batches')

    parser.add_argument('-p', '--particles',
                        action='store',
                        type=int,
                        default=10000,
                        help='Number of particles')

    parser.add_argument('-i', '--inactive',
                        action='store',
                        type=int,
                        default=10,
                        help='Number of inactive batches')

    parser.add_argument('--plotgeom',
                        action='store_true',
                        help='Plot geometry on defined planes')

    parser.add_argument('--planes',
                        action='store',
                        choices=['xy','yz','xz','vox'],
                        nargs='+',
                        default=['xy','yz','xz'],
                        help='''
                            2D-Planes for geometry plotting and mesh tallies.
                            If 'vox' argument provided, 3D-voxels are made
                            for ParaView vtk visualization.
                             ''')

    parser.add_argument('--meshsize',
                        action='store',
                        type=int,
                        default=250,
                        help='Mesh size resolution')

    parser.add_argument('--materialdata',
                        action='store',
                        choices=['msre','are','zpre'],
                        default='msre',
                        help='Reactor materials data. Defaults to MSRE')

    parser.add_argument('--localdata',
                        action='store',
                        type=Path,
                        default=None,
                        help='''
                            Path to local reactor materials data.
                            Can be .xml or .csv.
                            ''')

    parser.add_argument('--meshscores',
                        action='store',
                        choices=['flux','absorption','fission'],
                        nargs='+',
                        default=['flux','absorption','fission'],
                        help='Mesh scores to tally on planes')

    parser.add_argument('--coredim',
                        action='store',
                        type=int,
                        nargs='+',
                        default=[-80,-80,0,80,80,250],
                        help='''
                            Reactor core xyz dimensions space separated:
                            lower x, lower y, lower z,
                            upper x, upper y, upper z.
                            By default 'msre' reactor core dimension.
                              ''')
    parser.add_argument('--coreradius',
                        action='store',
                        type=float,
                        default=100,
                        help='Reactor core radius [cm]')

    parser.add_argument('--power',
                        action='store',
                        type=float,
                        default=10.0,
                        help='Reactor thermal power [MW]')

    parser.add_argument('--calcdose',
                        action='store_true',
                        help='''
                            Calculate dose.
                            Be aware that if dose calculation is enabled,
                            a detector need to be defined.
                            ''')

    parser.add_argument('--detmat',
                        action='store',
                        type=str,
                        default='icru',
                        help='''
                            Detector material for dose calculation.
                            Default is ICRU tissue composition.
                            ''')

    parser.add_argument('--detvol',
                        action='store',
                        type=float,
                        default=68508.936,
                        help='''
                            Detector volume.
                            Default is 68508.936[cm3], volume CAD phantom
                            human body.
                            ''')

    parser.add_argument('--particle',
                        action='store',
                        choices=['neutron','photon'],
                        nargs='+',
                        default=['neutron','photon'],
                        help='''
                            Particles to simulate.
                            Default is coupled neutron-photon.
                            ''')

    parser.add_argument('--calcreac',
                        action='store_true',
                        help='''
                            Calculate reaction rates.
                            If enabled, materials where to calculate
                            reaction rates need to be provided.
                            ''')

    parser.add_argument('--reacmat',
                        action='store',
                        nargs='+',
                        default=['blanket','fuel'],
                        help='Materials to calculate reaction rate on')

    args=parser.parse_args()

    if not Path(args.h5mfilename).is_file():
        raise FileNotFoundError(f"file {args.h5mfilename} not found.")

    return args
