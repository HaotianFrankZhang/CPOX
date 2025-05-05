#!/bin/bash

# Loop through each mutation folder
for folder in N272H_*
do
    # Loop through each run folder within the mutation folder
    for run in "$folder"/Run*
    do
        # Loop through each target folder (copro, uro) within the run folder
        for target in copro uro
        do
            # Change directory to the target folder
            cd "$run/$target"
            # Execute the sbatch command
            sbatch Vina_job
            # Return to the original directory
            cd - >/dev/null
        done
    done
done
