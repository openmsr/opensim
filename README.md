This Python package runs fully automatized OpenMC (Monte Carlo transport
code [OpenMC](https://github.com/openmc-dev/openmc)) simulations, with CAD based
geometries.

# Installation

```bash
pip install opensim
```

# Usage
To run OpenMC with this package a .h5m meshed geometrical model is needed.
To learn how to generate H5M meshes from CAD geometries and software required,
visit: [DAGMC website](https://svalinn.github.io/DAGMC/).

# How to run

Once installed, the package can be launched anywhere from the command-line typing
"simrun" followed by some command-line options. If no command-line options are
provided, default values are passed.

A DAGMC ".h5m" mesh geometry file needs to be provided, at least, to be able to
run the package.

Standard material libraries are built directly within the package, for three molten salt reactors:
- Molten Salt Reactor Experiment (msre)
- Aircraft Reactor Experiment (are)
- Zero Power Reactor Experiment (zpre)

Alternatively, materials can be defined locally as xml, csv or xlsx files.

# Arguments
See simrun --help for details on optional arguments.

- Mandatory arguments:

```bash
  --h5mfilename         Path to the .h5m file
```

- Optional arguments:
```bash
  -h, --help            show this help message and exit

  -r {run,plot-geom}, --runmode {run,plot-geom}
                        Choices: "run" or "plot-geometry"
                        Default: "run"
  -b BATCHES, --batches BATCHES
                        Number of batches
                        Default: 100
  -p PARTICLES, --particles PARTICLES
                        Number of particles
                        Default: 10000
  -i INACTIVE, --inactive INACTIVE
                        Number of inactive batches
                        Default: 10
  --plotgeom            Plot geometry during "run" mode

  --planes {xy,yz,xz,vox} [{xy,yz,xz,vox} ...]
                        2D-Planes for geometry plotting and mesh tallies. When
                        "vox" argument provided, 3D-voxels are made for
                        ParaView vtk visualization.
                        Default: 'xy','yz','xz'

  --materialdata        
                        Reactor materials data tables
                        Choices: 'msre','are', 'zpre'
                        Default: msre
  --localdata           Path to local reactor materials data.
                        Can be .xml .csv or .xmls
  --meshscores {flux,absorption,fission} [{flux,absorption,fission} ...]
                        Mesh scores to tally on planes
                        Default: 'flux','absorption','fission'
  --coredim COREDIM [COREDIM ...]
                        Reactor core xyz dimensions in cm, space separated, in the order:
                        lower x,lower y, lower z, upper x, upper y, upper z.
                        Default is 'MSRE' reactor core dimension.
  --power POWER         Reactor thermal power [MW] for units conversion.    
                        Default: 100
  --calcdose            If provided, calculate dose on defined detector.

  --detmat DETMAT       Detector material for dose calculation.
                        Default: ICRU tissue composition.
  --detvol DETVOL       Detector volume.
                        Default is 68508.936 [cm3], corresponing to the
                        volume of GrabCAD human phantom.
  --particle {neutron,photon} [{neutron,photon} ...]
                        Particles to simulate.
                        Default: coupled neutron-photon transport.
  --calcreac            If provided, calculate reaction rates on specified
  --detmat DETMAT       Detector material for dose calculation.
                        Default: ICRU tissue composition.
  --detvol DETVOL       Detector volume.
                        Default is 68508.936 [cm3], corresponing to the
                        volume of GrabCAD human phantom.
  --particle {neutron,photon} [{neutron,photon} ...]
                        Particles to simulate.
                        Default: coupled neutron-photon transport.
  --calcreac            If provided, calculate reaction rates on specified

                        materials.
  --reacmat REACMAT [REACMAT ...]
                        Material names where to calculate reaction rates.                  

```
# Molten Salt Reactor Experiment (msre) example
Runs msre.h5m mesh file with 100000 neutrons particles and 100 batches. Coredim takes the
dimension of the reactor vessel for initializing neutron distribution. Providing plotgeom argument
will plot the geometry on xy,yz,zx planes (by deafult) during "run" mode. The MSRE defautl material data are passed.
Meshscores argument will score provided tallies on the default planes.

```bash
simrun msre.h5m -p 1000000 -b 100 --coredim -75 -75 0 75 75 250 --plotgeom
--materialdata msre --meshscores flux absorption fission
```
For further details on how to run the msre and a download for the h5m file, see the [examples](https://github.com/openmsr/opensim/tree/main/examples).
