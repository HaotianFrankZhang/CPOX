import MDAnalysis as mda
from MDAnalysis.coordinates.PDB import PDBWriter
import os
import subprocess
import os

def cleanTraj(u, currDirectory):
    try:
        selection_str = "not (resname TIP3 or resname HOH or resname POT or resname CLA)"
        # Adjusting selection to keep only the desired atoms
        selected_atoms = u.select_atoms(selection_str)

        # Writing the cleaned-up structure to new PSF and PDB files
        # selected_atoms.write(currDirectory + 'cleaned_structure.psf')
        selected_atoms.write(currDirectory + 'step3_input.pdb')

        # Re-selecting atoms using the cleaned structure as topology
        selected_atoms = u.select_atoms(selection_str)
        # Writing out the cleaned trajectory
        with mda.Writer(currDirectory + 'step5_1.dcd', selected_atoms.n_atoms) as W:
            for ts in u.trajectory:
                W.write(selected_atoms)
    except:
        print("Selection error")

def writeFrame(currMutation, currRun):
    # Load the trajectory
    currDirectory = './' + currMutation + '/' + currRun + '/'
    u = mda.Universe(currDirectory + 'step3_input.psf', currDirectory + 'step5_continue.dcd')
    # cleanTraj(u, currDirectory)


    if not os.path.exists('./' + currMutation + '/' + currRun + '_frame'):
        os.makedirs('./' + currMutation + '/' + currRun + '_frame')

    # cleanTraj(u, currDirectory)
    # This example keeps protein and not solvent ('resname SOL') or common ions ('resname NA CL')
    protein = u.select_atoms("protein and not resname POT and not resname CLA")

    # Loop through each frame of the trajectory
    for frame in range(len(u.trajectory)):
        u.trajectory[frame]  # Update the trajecto
        # Generate the filename for each frame
        filename = './' + currMutation + '/' + currRun + '_frame/' + f"frame_{frame + 1:04d}.pdb"
        # Write the current frame to a PDB file
        with PDBWriter(filename, multiframe=False) as pdb_writer:
            pdb_writer.write(protein)

    print("Finished extracting all frames.")

def main():


    # Mutation = ['WT'] # ['G188Q', 'L155W', 'V135A']
    Mutation = ['WT', 'N272H', 'L155W', 'G188Q', 'V135A']
    Run = ['Run1', 'Run2', 'Run3', 'Run4', 'Run5'] # ['Run1', 'Run2']
    # Run = ['200ns']

    for currMutation in Mutation:
        for currRun in Run:
            # print ('./' + currMutation + '/' + currRun + '/')
            writeFrame(currMutation, currRun)

if "__name__" == main():
    main()
    
