timeoutS=900  # timeout in seconds
iter=1   # number of iterations, to eventually take randomness into account

launch_solver="scripts/minizinc/process_minizinc.sh"

currentDate=$(date +%Y-%m-%d_%H-%M-%S);  #
gitShortHash=$(git rev-parse --short HEAD)
outFileOpt="results/minizinc/minizinc-${currentDate}-${gitShortHash}.csv"
mkdir -p "results/minizinc"  # where the results will be written
rm -f $outFileOpt  # delete filename of the results if it already existed (does not delete past results, unless their datetime is the same)

echo "solver,model,instance,timeLimitS,seed,status,runTimeS,nodes,failures,seq,args" >> $outFileOpt

#declare -a solvers=("org.minizinc.mip.gurobi" "org.minizinc.mip.scip" "org.minizinc.mip.highs")  # mip family
#declare -a solvers=("gecode" "cp-sat" "chuffed")  # CP / CP-SAT family
declare -a solvers=("gecode" "cp-sat" "chuffed" "org.minizinc.mip.highs")  # many categories
declare -a models=("models/model1.mzn" "models/model6.mzn" "models/model_template.mzn")
inputFile="inputFileMinizinc"
rm -f $inputFile  # delete previous temporary file if it existed

echo "writing inputs"
for (( i=1; i<=$iter; i++ ))  # for each iteration
do
  for model in "${models[@]}"  # for each model
    do
      for solver in "${solvers[@]}"  # for each solver
      do  # write a line being part of the inputs used to launch experiments (instance,solver,model)
        find instances -type f | sed "s|$|,$solver,$model|" >> $inputFile
      done
  done
done

# add a comma and a random seed at the end of each line
awk -v seed=$RANDOM '{
    srand(seed + NR); # seed the random number generator with a combination of $RANDOM and the current record number
    rand_num = int(rand() * 10000); # generate a random number. Adjust the multiplier for the desired range.
    print $0 "," rand_num;
}' $inputFile | sponge $inputFile
echo "launching experiments in parallel"
cat $inputFile | parallel -j 25 --colsep ',' $launch_solver {2} {3} {1} $timeoutS {4} >> $outFileOpt
echo "experiments have been run"
echo "results have been written to file $outFileOpt"
rm -f $inputFile
