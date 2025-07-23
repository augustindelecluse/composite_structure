# csp_composite_structures

Minizinc models, instances and checker to solve a composite structure design problem.

The problem and approach are described in Antoons, M., Delecluse, A., Zein, S., & Schaus, P. (2025). Modeling and Solving a Composite Structure Design Problem with Constraint Programming. In *31st International Conference on Principles and Practice of Constraint Programming (CP 2025)*. Schloss Dagstuhl–Leibniz-Zentrum für Informatik.

- The minizinc models are located in the `models` directory. Differences between each model are explained [at the bottom of this file](#minizinc-models).
- The minizinc instances are located in the `instances` directory. Each subdirectory contains different size of instances.
- Scripts to easily launch experiments are located in the `experiments` directory.
- Solution checker is within the `checker` directory.

## Launching experiments

*Requirements*

- `minizinc` to run the minizinc models
- `gnu parallel` to launch the experiments in parallel

All scripts are supposed to be launched from the root of the project

Solving an instance can be done by the command

```
./experiments/process_minizinc.sh <solver> <model> <instance> <timeLimit> <seed>
```

Where

- `solver` describe the minizinc backend solver to use
- `model` refers to the minizinc model `.mzn` file
- `instance` refers to the minizinc instance `.dzn` file
- `timeLimit` is the timeout, in seconds
- `seed` is a random seed, given in seconds

This command produces an output in one line, containing values separated by commas `,`, with the following format:

```
solver,model,instance,timeLimitS,seed,status,runTimeS,nodes,failures,seq,args
```

Where

- the first 5 values are the ones given in input
- `status` is the solving status: `SATISFIABLE`, `UNSATISFIABLE`, `UNKNOWN` or `UNDETERMINED`
- `runTimeS` is the run time, in seconds
- `nodes` is the number of nodes in the search tree
- `failures` is the number of failures encountered in the search tree
- `seq` is a string describing the solution, in one line. It is empty unless a solution has been found.
- `args` is the exact command used within the script to launch minizinc

### Example

The command

```
./experiments/process_minizinc.sh chuffed models/model1.mzn instances/3x3/random_grid_bench_3_3_009.dzn 5 10
```

Produces an output similar to

```
chuffed,model1.mzn,random_grid_bench_3_3_009.dzn,5.000,10,SATISFIABLE,0.052,1480,453,seq = [| 1 2 2 2 1 4 1 2 2 2 1 4 4 4 3 4 3 4 4 4 3 4 4 3 2 2 3 4 4 3 4 4 4 3 4 3 4 4 4 1 2 2 2 1 4 1 2 2 2 1 | 1 2 2 1 4 1 2 2 1 4 4 4 3 4 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 4 3 4 4 4 1 2 2 1 4 1 2 2 1 0 0 0 0 0 0 | 1 2 2 1 4 1 2 1 4 4 4 3 4 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 4 3 4 4 4 1 2 1 4 1 2 2 1 0 0 0 0 0 0 0 0 | 1 2 2 1 4 1 2 2 2 1 4 4 3 4 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 4 3 4 4 1 2 2 2 1 4 1 2 2 1 0 0 0 0 0 0 | 1 2 2 1 4 1 2 1 4 4 3 4 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 4 3 4 4 1 2 1 4 1 2 2 1 0 0 0 0 0 0 0 0 0 0 | 1 2 2 1 4 1 2 1 4 4 3 4 3 4 4 4 3 4 3 3 4 3 4 4 4 3 4 3 4 4 1 2 1 4 1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 | 1 2 2 1 4 1 2 2 1 4 4 3 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 3 4 4 1 2 2 1 4 1 2 2 1 0 0 0 0 0 0 0 0 0 0 | 1 2 2 1 4 1 2 1 4 4 3 3 4 4 4 3 4 3 2 2 3 4 3 4 4 4 3 3 4 4 1 2 1 4 1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 | 1 2 2 1 4 1 1 4 4 3 3 4 4 3 4 3 3 4 3 4 4 3 3 4 4 1 1 4 1 2 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 |],minizinc --time-limit 5000 --solver chuffed models/model1.mzn instances/3x3/random_grid_bench_3_3_009.dzn --statistics -r 102
```

### Launching in parallel

A batch of experiments can be directly launched by invoking the script `./experiments/run_minizinc_parallel.sh`.
Experiments are launched in parallel.
Please refer directly to the script to change settings (adapt timeout, set of instances, models to run, etc.).

## Constraints

### Mandatory

- **B1**: Blending Constraint
- **B2**: No Ply Crossing Constraint
- **B3**: Continuous Surface Plies Constraint
- **B4**: A maximum dropoff of 3 consecutive layers is allowed between 2 sequences
- **D1**: A given number of plies must be present in every sequence

### Optional

- **D2**: Angle difference cannot be equal to 90°
- **D3**: Maximum 3 consecutive plies with the same angle
- **D4**: Vertical Symmetry Constraint with the exception of a dysymmetry in th middle 2 or 3 plies in an even or odd thickness respectively
- **D5**: Surface plies can only take -45°/45° angle

## MiniZinc Models

Different models, each with their own set of constraints are available for the paper [here](./models).
The different models and their set of constraints are

- [A template model](./models/model_template.mzn) this model only contains the constraints that are always activated. Those are the **blending constraint** (B1), the **no-ply-crossing constraint** (B2), the cardinality constraint enforcing a **given amount of every ply direction in each sequence** (D1), the constraint enforcing **no ply drop-offs for the surface plies** (B3) and the constraint enforcing **a maximum drop-off of 4 consecutive plies between two sequences** (B4).
- [Model 1](./models/model1.mzn) which activates all constraints available.
- [Model 2](./models/model2.mzn) adds the constraint prohibiting 90° gaps between plies in every sequence (D2).
- [Model 3](./models/model3.mzn) adds the constraint that disallows 3 consecutive plies of the same angle in every sequence (D3).
- [Model 4](./models/model4.mzn) adds the constraint enforcing that every sequence must be vertically symmetric (D4).
- [Model 5](./models/model5.mzn) adds the constraint that allows the surface plies (top and bottom) to only take the -45° and 45° angles (D5).
- [Model 6](./models/model6.mzn) adds the symmetric sequences constraint and the constraint prohibiting 4 or more consecutive plies of the same direction (D3, D4).
- [Model 7](./models/model7.mzn) all optional constraint but the symmetry constraint (D2, D3, D5).

## Checker

A checker is available in the [checker](checker) directory to check the validity of a solution.
It requires Python 3 to run, but no additional dependencies need to be installed.
It can be launched from the root directory of the project with the command

```sh
python3 checker/main.py <instance_file> <solution_file>
```

Where `instance_file` is the path to the instance file and `solution_file` is the path to the solution file.

The script also accepts the optional command `--verbose` for a detailed output.

### Format of the Instance File

The input file must be in .dzn format and must contain the following elements:
- edges: an array of tuples that represents the edges from the input graph.
  The first element of the tuple is the parent (thickest sequence) while the second element is the child.
  EXAMPLE: if we have the graph 0 -> 1 -> 2, the edges array will be:
  `edges = [(0, 1), (1, 2)];`
- counts: an array of arrays that represents the number of plies for each angle that must be present in
  each stacking sequence.
  Every sub-array must have 4 values (one for each angle).
  EXAMPLE: the counts array for a structure with two sequences should look like this:
  `counts = [|1, 2, 3, 4,|2, 3, 1, 0,|];`

An example of a full instance file can be found [here](instances/3x3/random_grid_bench_3_3_173.dzn).

### Format of the Solution File

The solution file must be in .dzn format and must follow one of 2 formats:
- The first contains two 2D arrays: seqs and indexes.
  The sequences array contains the stacking sequences, while the indexes array contains the indexes of the
  plies in the sequences. All the sub arrays (for the sequences AND the indexes) must be of the same
  length, which is the length of the thickest stacking sequence.  
  EXAMPLE:
    ```dzn
    seqs = [|1, 2, 3, 4|2, 3, 1, 0|];
    indexes = [|0, 1, 2, 3|0, 1, 2, 3|];
    ```
  A more complete example of this format can be found [here](checker/example_solution.dzn).
- The second contains a separate 1D array for each stacking sequence and for the indexes of the plies.
  The sequences array contains the stacking sequences, while the indexes array contains the indexes of the
  plies in the sequences. The arrays are allowed to be of different length.  
  EXAMPLE:
    ```dzn
    seq0 = [1, 2, 3, 4];
    seq1 = [2, 3, 1];
    ...
    i0 = [0, 1, 2, 3];
    i1 = [0, 1, 2, 3];
    ...
    ```
### Example

The command

```sh
python3 checker/main.py instances/3x3/random_grid_bench_3_3_173.dzn checker/example_solution.dzn
```

Launched from the root of this project should pass all the constraint checks and gives an output similar to:

```
Report of checks:
-----------------
B1: PASSED
B2: PASSED
B3: PASSED
B4: PASSED
D1: PASSED
D2: PASSED
D3: PASSED
D4: PASSED
D5: PASSED
-----------------
```
