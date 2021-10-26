#!/bin/sh

for cores in 4 8 16 32
do
  for nodes in 4 8 16 32
  do
    CMD="python3 distrdf.py -c ${cores}  -N ${nodes}"
    printf "\n\n${CMD}\n" >> ~/distrdf_timestamps.out
    eval "$CMD"
    echo "$CMD was done"
  done
done

