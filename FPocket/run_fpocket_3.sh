#!/bin/bash

# Base directory where your directories are located
BASE_DIR="."

# Array of directories to process
DIRS=("G188Q" "L155W" "V135A" "N272H" "WT")
# DIRS=("N272H")

# Iterate over each directory
for dir in ${DIRS[@]}; do
    # Iterate over each run within the directory
    for run in Run1_frame Run2_frame Run3_frame Run4_frame Run5_frame; do
        # Define FRAME_DIR and OUTPUT_DIR for the current run
        FRAME_DIR="${BASE_DIR}/${dir}/${run}"
        # OUTPUT_DIR="${BASE_DIR}/${dir}/${run}_output"

        # Make sure the output directory exists
        # mkdir -p ${OUTPUT_DIR}

        # Iterate over each PDB file in the FRAME_DIR
        for pdb in ${FRAME_DIR}/*.pdb; do
            echo "Processing ${pdb}"
            # Run Fpocket on the PDB file
            fpocket -f ${pdb} 
        done
    done
done

echo "Processing complete."
