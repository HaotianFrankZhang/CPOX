# MD_analysis / AF_analysis

This folder contains scripts and Jupyter notebooks used for the analysis of molecular dynamics (MD) simulations based on AlphaFold-predicted CPOX structures, as part of the study:  
**"Environment-dependent landscapes of coding variant impacts on coproporphyrinogen oxidase"**

## 📁 Folder Structure

- `AF_analysis/`
  - `CalcDistances.ipynb`: Computes pairwise Cα distances between key residues across MD trajectories.
  - `MD_MSF.ipynb`: Calculates mean square fluctuations (MSF) for each residue to assess flexibility.

---

## 📦 Required Packages

To run the notebooks in this folder, you will need the following Python packages:

```bash
pip install numpy pandas matplotlib mdtraj mdanalysis
