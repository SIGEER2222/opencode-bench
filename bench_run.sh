#!/bin/bash
OUT=/tmp/bench
mkdir -p "$OUT"
INTEL=$(cat bench_prompt_intel.txt)
SPEED=$(cat bench_prompt_speed.txt)
export OUT INTEL SPEED

run_one() {
  local model="$1" tag="$2" prompt="$3"
  local safe=$(echo "$model" | tr '/' '_')
  local f="$OUT/${safe}.${tag}.jsonl"
  local t0=$(date +%s.%N)
  timeout 240 opencode run --format json -m "$model" "$prompt" > "$f" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  echo "$rc $(echo "$t1 - $t0" | bc)" > "$OUT/${safe}.${tag}.meta"
}
export -f run_one

xargs -P 3 -I{} bash -c 'echo "START {}"; run_one "{}" intel "$INTEL"; run_one "{}" speed "$SPEED"; echo "DONE {}"' < bench_models.txt
echo "ALL DONE"
