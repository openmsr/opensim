#!/bin/bash

#run with default msre material data library
simrun --h5mfilename msre.h5m -p 1000000 -b 100 --coredim -75 -75 0 75 75 250 --plotgeom --materialdata msre --meshscores flux absorption fission
