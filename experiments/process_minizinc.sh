#!/usr/bin/env bash

# Ensure we have exactly 5 arguments
if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <solver> <model> <instance> <timeLimitInSeconds> <seed>"
  exit 1
fi

solver="$1"
model="$2"
instance="$3"
timeLimitInSeconds="$4"
seed="$5"
# echo "$solver $model $instance $timeLimitInSeconds $seed"

# Convert time limit from seconds to milliseconds
timeLimitMS=$(( timeLimitInSeconds * 1000 ))

# Run MiniZinc and capture stdout + stderr
output=$(minizinc --time-limit "$timeLimitMS" \
                  --solver "$solver" \
                  "$model" \
                  "$instance" \
                  --statistics \
                  -r "$seed" 2>&1)
command_str="minizinc --time-limit $timeLimitMS --solver $solver $model $instance --statistics -r $seed"

# --- Determine status ---
# You can expand or change these checks as needed, depending on the solver outputs you expect.
if echo "$output" | grep -q "=====UNSATISFIABLE====="; then
    status="UNSATISFIABLE"
elif echo "$output" | grep -q "seq ="; then
    status="SATISFIABLE"
elif echo "$output" | grep -q "=====OPTIMAL====="; then
    status="OPTIMAL"
elif echo "$output" | grep -q "=====UNKNOWN====="; then
    status="UNKNOWN"
elif echo "$output" | grep -q "=====SOLVE TIMEOUT====="; then
    status="TIMEOUT"
else
    # If none of the above markers is found, we'll mark it as "UNDETERMINED"
    status="UNDETERMINED"
fi

# --- Extract statistics ---
# We'll use sed to extract the numeric values after each keyword.

timeValue=$(echo "$output"     | sed -n 's/%%%mzn-stat: solveTime=\(.*\)/\1/pi' | head -n1 | xargs)
nodes=$(echo "$output"         | sed -n 's/%%%mzn-stat: nodes=\(.*\)/\1/p' | head -n1 | xargs)
failures=$(echo "$output"      | sed -n 's/%%%mzn-stat: failures=\(.*\)/\1/p' | head -n1 | xargs)

# If any of them doesn't appear in the output, default to 0 or empty
timeValue="${timeValue:-0}"
nodes="${nodes:-0}"
failures="${failures:-0}"

# --- Extract seq (if status is SATISFIABLE or OPTIMAL) ---
# We'll look for lines between 'seq =' and '];',
# remove all newlines, replace "];" with "]", and remove all commas.
seqValue=""
if [ "$status" = "SATISFIABLE" ] || [ "$status" = "OPTIMAL" ]; then
  seqValue=$(echo "$output" \
    | sed -n '/seq =/,/\];/p'  \
    | tr -d '\n'               \
    | sed 's/];/]/'           \
    | sed 's/,//g')
fi

instanceShortened=$(basename "$instance")
modelShortened=$(basename "$model")
timeLimitSecFormatted=$(printf "%.3f" "$timeLimitInSeconds")
runTimeSecFormatted=$(printf "%.3f" "$timeValue")

# --- Print summary line ---
# The order is:
#   solver , model , instance , timeLimitS , seed , status , runTimeS , nodes , failures , sequence
echo "${solver},${modelShortened},${instanceShortened},${timeLimitSecFormatted},${seed},${status},${timeValue},${nodes},${failures},${seqValue},${command_str}"
