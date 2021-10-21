#!/bin/sh

for Nodes in 1 2 4:
do
    for ntasks in 1 2 4 8:
    do
        for cores in 1 2 4 8:
        do
            CMD="python3 distrdf.py -c $cores -n $ntasks -N $Nodes"
            printf "\n\n${CMD}\n" >> ~/distrdf_timestamps.out
            JID=$(eval "$CMD" 2>&1 | tail -n1 | awk '{print $NF}')
            printf "\n" >> ~/distrdf_timestamps.out
            scontrol -d show job $JID >> ~/distrdf_timestamps.out
            cat slurm-${JID}.out >> ~/distrdf_timestamps.out
            echo "$CMD was done"
        done
    done
done

