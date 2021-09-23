#!/bin/bash

PYTHON=`which python3`
PYTHONPATH=benchmarks:$PYTHONPATH

NPARTITIONS=1
TIMES_DIR=time_results
NTESTS=1

mkdir -p $TIMES_DIR

# df102
for benchmark_name in df102_NanoAODDimuonAnalysis df103_NanoAODHiggsAnalysis df104_HiggsToTwoPhotons
do
  echo "Running $benchmark_name"
  for mode in "" "--optimized"
  do
    TIME_FILENAME=$TIMES_DIR/${benchmark_name}_${mode}_${NPARTITIONS}
    for i in `seq $NTESTS`
    do
      $PYTHON launch.py --benchmark $benchmark_name --npartitions $NPARTITIONS $mode 1>> ${TIME_FILENAME}.out 2>> ${TIME_FILENAME}.err
    done
  done
done

# Cleanup
rm -f rdfworkflow_*
rm *.pdf 
