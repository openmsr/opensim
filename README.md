This Python package automatically runs OpenMC Monte Carlo transport simulation
code [OpenMC](https://github.com/openmc-dev/openmc) with CAD based geometry.

# Installation

```bash
pip install opensim/
```

# Usage
To run OpenMC with this package a geometry H5M file is needed. To learn how to
generate a H5M file from a CAD geometry and software requirements,
please visit: [DAGMC website](https://svalinn.github.io/DAGMC/).

# How to run
The package can be launched from the command-line typing "simrun".

A previously generated DAGMC .h5m geometry file needs to provided as
positional argument.

# Arguments
See simrun --help

- Positional arguments:

```bash
  path                  the path to a h5m file
```

- Optional arguments:
```bash
  -h, --help            show this help message and exit

  -r {run,plot-geom}, --runmode {run,plot-geom}
                        Run mode: "run" or "plot-geometry"
  -b BATCHES, --batches BATCHES
                        Number of batches
  -p PARTICLES, --particles PARTICLES
                        Number of particles
  -i INACTIVE, --inactive INACTIVE
                        Number of inactive batches
  --plotgeom            Plot geometry on defined planes

  --planes {xy,yz,xz,vox} [{xy,yz,xz,vox} ...]
                        2D-Planes for geometry plotting and mesh tallies. When
                        "vox" argument provided, 3D-voxels are made for
                        ParaView vtk visualization.

  --meshsize MESHSIZE   Mesh size resolution
  --materialdata    
                        Reactor materials data
  --meshscores {flux,absorption,fission} [{flux,absorption,fission} ...]
                        Mesh scores to tally on planes
  --coredim COREDIM [COREDIM ...]
                        Reactor core xyz dimensions space separated, in the order:
                        lower x,lower y, lower z, upper x, upper y, upper z.
                        Default is 'MSRE' reactor core dimension.
  --power POWER         Reactor thermal power [MW] for units conversion.
  --calcdose            If provided, calculate dose on defined detector.
  --detmat DETMAT       Detector material for dose calculation. Default is
                        ICRU tissue composition.
  --detvol DETVOL       Detector volume. Default is 68508.936 [cm3], volume of CAD
                        phantom human body.
  --particle {neutron,photon} [{neutron,photon} ...]
                        Particles to simulate. Default is coupled neutron-
                        photon transport.
  --calcreac            If provided, calculate reaction rates on specified 
                        materials.
  --reacmat REACMAT [REACMAT ...]
                        Materials where to calculate reaction rates.                  

```
# MSRE example
Will run msre.h5m geometry file, with 100000 particles and 100 batches. Coredim takes the
dimension of the reactor vessel for initializing neutron distribution. Providing plotgeom argument
will plot the geometry on xy,yz,zx planes (by deafult). The appropriate MSRE package material data is gievn.
Meshscores argument will score provided tallies on the default planes.

```bash
simrun msre.h5m -p 1000000 -b 100 --coredim -75 -75 0 75 75 250 --plotgeom
--materialdata msre --meshscores flux absorption fission
```
