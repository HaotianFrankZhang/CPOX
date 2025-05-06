# CPOX Dynamics and Pocket Analysis

This folder contains scripts and Jupyter notebooks used for the analysis of molecular dynamics (MD) simulations based on AlphaFold-predicted CPOX structures, as part of the study:

**"Environment-dependent landscapes of coding variant impacts on coproporphyrinogen oxidase"**

## 📁 Folder Structure

```
.
├── FPocket/
├── Hinge_analysis/
├── MD_analysis/
│   ├── AF_analysis/
│   └── Crystal_analysis/
├── PCA_analysis/
```

---

## 🔹 FPocket/

**Purpose:** Identify and evaluate ligand-binding pockets across MD snapshots and CPOX variants using [fpocket](https://github.com/Discngine/fpocket).

### Files & Steps:
- `Ref_Pocket1.txt`, `Ref_Pocket2.txt`: Lists of reference residues for pockets of interest.
- `GetReferencePoket_1.py`: Define and validate pocket residues from initial structures.
- `prepareFpocket_2.py`: Extract individual PDB frames from MD trajectories.
- `run_fpocket_3.sh`: Run fpocket on each frame to detect binding pockets.
- `ScreenPocket_4.py`: Compare detected pockets to references based on residue overlap.
- `Pick_pocket_5.py`: Extract physiochemical features (e.g., volume, polarity) of pockets of interest.

### Dependencies:
```bash
pip install MDAnalysis
pip install prodigy-prot
```

- Requires installation of [fpocket](https://github.com/Discngine/fpocket) binary.
- Uses [PRODIGY](https://github.com/haddocking/prodigy) for optional pocket affinity prediction.

---

## 🔹 Hinge_analysis/

**Purpose:** Identify global hinge sites—key pivot points involved in collective motions—using normal mode analysis.

### Files:
- `CPOX_AF.pdb`: Reference AlphaFold structure of CPOX.
- `find_hinges.ipynb`: Builds structural ensemble, performs GNM/ANM, and detects hinge sites.

### Dependencies:
```bash
pip install prody numpy matplotlib
```

**Citation:**  
Bahar I. et al., *Global hinge sites of proteins as target sites for drug binding*

---

## 🔹 MD_analysis/

**Purpose:** Analyze dynamics across AlphaFold-based and crystal-based MD simulations.

### Subfolders:
- `AF_analysis/`
  - `calcDIstances.ipynb`: Calculates inter-residue distances across frames.
  - `MD_MSF.ipynb`: Computes Mean Square Fluctuations (MSF).
- `Crystal_analysis/`: Mirror structure for crystal-based systems.

### Dependencies:
```bash
pip install MDAnalysis prody matplotlib pandas seaborn numpy
```

---

## 🔹 PCA_analysis/

**Purpose:** Perform Principal Component Analysis (PCA) to evaluate dominant motions and compare conformational sampling.

### Files:
- `EvalMD_PCA_crystal.ipynb`: PCA for crystal MD systems.
- `EvalMD_PCA_WT.ipynb`: PCA for AlphaFold MD systems.
- `AF_plots/`: Plots from AlphaFold-based PCA.
- `Crystal_plots/`: Plots from crystal-based PCA.

### Dependencies:
```bash
pip install MDAnalysis prody matplotlib pandas seaborn numpy
```

---

## 📚 Citations

- **PRODIGY**: [https://github.com/haddocking/prodigy](https://github.com/haddocking/prodigy)  
- **Hinge site analysis**: Haotian Z. et al., *Global hinge sites of proteins as target sites for drug binding*

---

## 📬 Contact

For questions or collaboration inquiries, please contact:  
**Haotian Zhang** — haz100@pitt.edu
