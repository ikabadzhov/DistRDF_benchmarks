#!/bin/sh

while getopts c:n:N: flag
do
    case "${flag}" in
        c) cores=${OPTARG};;
        n) ntasks=${OPTARG};;
        N) Nodes=${OPTARG};;
    esac
done

CMD="python3 distrdf.py -c $cores -n $ntasks -N $Nodes"
printf "\n\n${CMD}\n" >> ~/distrdf_timestamps.out

JID=$(eval "$CMD" 2>&1 | tail -n1 | awk '{print $NF}')
printf "\n" >> ~/distrdf_timestamps.out
scontrol -d show job $JID >> ~/distrdf_timestamps.out
cat slurm-${JID}.out >> ~/distrdf_timestamps.out
