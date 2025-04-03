# csp_composite_structures

Minizinc models and instances to solve a composite structure design problem.

- The minizinc models are located in the `models` directory. Differences between each model are explained [at the bottom of this file](#minizinc-models).
- The minizinc instances are located in the `instances` directory. Each subdirectory contains different size of instances.
- Scripts to easily launch experiments are located in the `experiments` directory.

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
- **D6**: Uniform distribution of 0° and 90° plies

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
