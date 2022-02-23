#!/bin/bash

#run with local material data definition
simrun --h5mfilename msre.h5m -p 1000000 -b 100 --coredim -75 -75 0 75 75 250 --plotgeom --localdata mat_msre --meshscores flux absorption fission
