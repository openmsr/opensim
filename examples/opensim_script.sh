#!/bin/bash
################################################################################
######Shell script to run multiple Openmc simulation using simrun package#######
################################################################################

# Define associative (-A) arrays.
# Simulation [arguments] need to match the parse arguments in opensim.
# Order is not important, neither array name definition

declare -A run1=(
  [h5mfilename]='msre/msre.h5m' #path to h5m file
  [localdata]='/msre/mat_msre' #path to local material data
  [particles]=1000000
  [batches]=100
  [coredim]='0 75 75 250'
  [meshscores]='flux absorption fission'
)
declare -A run2=(
  [h5mfilename]='msre/msre.h5m' #path to h5m file
  [materialdata]='msre' #msre default library
  [particles]=1000000
  [batches]=100
  [coredim]='0 75 75 250'
  [meshscores]='flux absorption fission'
)


# Iterate over the arrays
for i in ${!run@}; do
  echo "Start of run: $i"

  # create directory for new simulation, if doesn't exist
  newdir="${i}_$(date +%F)"
  echo $newdir
  [ ! -d $newdir ] && mkdir $newdir
  cd $newdir

  #delete old simulations result files, if present
  old=(*.xml *.h5 *.png *ppm *.out)
  for f in ${old[@]}; do
    if ls $f >/dev/null 2>&1; then
      echo $f
      rm $f
    fi
  done

  # we need to do this to iterate over an array
  declare -n run=$i

  # loop over run arguments and store keys and values into a string.
  arg_list=""
  for p in ${!run[@]}; do
    arg_list+=$"--$p ${run[$p]} "
  done

  # run simrun with whtever arguments defined in the simulation run array
  simrun $arg_list
  echo "End of run: $i"

  cd ..
done
