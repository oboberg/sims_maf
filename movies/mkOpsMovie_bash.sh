#!/bin/bash

## This script will generate but NOT run the commands to create movies for a series of nights from an opsim run.
## The outputs for each night will be stored in opsRun_nX (including the movie from each individual night).

## usage: mkOpsMovie.sh [opsim name] [night start] [night end]
## after generating the movies for each individual night, join the movies together using joinOpsMovie.sh


opsRun=$1
nightStart=$2
nightEnd=$3
echo "#Making movie from " $opsRun " for nights " $nightStart " to " $nightEnd

# if ($4) then
#    set sqlconstraint = $4" and"
#    echo " using general sqlconstraint " $sqlconstraint
# else
#    set sqlconstraint = ''
# endif


# nights=`seq $nightStart $nightEnd`
for night in `seq $nightStart $nightEnd`; do
    nightconstraint=$sqlconstraint" night="$night
    echo "python opsimMovie.py "$opsRun".db --sqlConstraint "$nightconstraint" --ips 30 --addPreviousObs --outDir "$opsRun"_n"$night
done
