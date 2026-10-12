#!/bin/bash
# Shard driver: runs v2 settings in priority order with an overall time
# budget; fully resumable across repeated invocations.
# Priority: E-A fmnist B60 k3 -> E-B mnist B60 k3 -> E-C fmnist B30 k3
#           -> E-E fmnist B60 k5 -> E-D fmnist B120 k3
BUDGET=${1:-540}
ST="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$ST/.." && pwd)"
OUT="$ROOT/results/v2"
mkdir -p $OUT
cd $ST

run() {  # id budget k out
  echo "### setting: $1 B=$2 k=$3 -> $4 (elapsed ${SECONDS}s)"
  python3 run_experiments_v2.py --id "$1" --budget "$2" --k "$3" \
      --seeds 0:10 --out "$4" --time-budget $(( BUDGET - SECONDS ))
  rc=$?
  if [ $rc -eq 0 ]; then echo "### DONE: $4"; return 0; fi
  if [ $rc -eq 42 ]; then echo "### UNFINISHED: $4 (will resume next shard)"; exit 42; fi
  echo "### ERROR rc=$rc in $4"; exit $rc
}

SECONDS=0
run fmnist 60 3 $OUT/experiment_v2_fmnist_B60_k3.jsonl || exit $?
run mnist  60 3 $OUT/experiment_v2_mnist_B60_k3.jsonl || exit $?
run fmnist 30 3 $OUT/experiment_v2_fmnist_B30_k3.jsonl || exit $?
run fmnist 60 5 $OUT/experiment_v2_fmnist_B60_k5.jsonl || exit $?
run fmnist 120 3 $OUT/experiment_v2_fmnist_B120_k3.jsonl || exit $?
echo "### ALL SETTINGS COMPLETE ($(date))"
