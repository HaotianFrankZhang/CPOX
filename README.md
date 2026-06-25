# Environment-dependent landscapes of coding variant impacts on coproporphyrinogen oxidase

This repository contains the necessary notebooks, scripts, processed datasets, and analysis outputs used to perform nearly all analyses described in the manuscript:

**"Environment-dependent landscapes of coding variant impacts on coproporphyrinogen oxidase"**

---

## 📁 Folder Structure

```text
.
├── BioData/
├── FPocket/
├── Hinge_analysis/
├── MD_analysis/
│   ├── AF_analysis/
│   └── Crystal_analysis/
├── PCA_analysis/
├── Docking_data/
├── prodigy-lig/
└── Ori_data/
```

---

## 🔹 BioData

**Purpose:** Store processed biological datasets and R code used to generate most manuscript figures related to variant effect map scores and biological interpretation.

### Files:

* `Manuscript_Data.xlsx`: A single Excel workbook containing processed data and supplementary resources supporting the manuscript. This includes variant effect map scores under baseline and mercury-treated conditions, delta scores, log likelihood ratios of pathogenicity, a curated clinical reference set, in silico predictions including AlphaMissense, ΔΔG, and SASA, enzymatic activity measurements, and oligonucleotide sequences used for mutagenesis and sequencing.

* `CPOX_Manuscript_Rcode_v3.Rmd`: R Markdown file used to generate nearly all figures related to the variant effect map scores in the manuscript.

### Dependencies:

* R version 3.6.3 or higher
* OpenPyMOL 1.8 or higher

Many scripts in this repository depend on the R packages listed below. Please install them before running the analysis.

```r
install.packages(c(
  "cowplot",
  "data.table",
  "ggnewscale",
  "ggplot2",
  "ggpubr",
  "ggrepel",
  "ggsignif",
  "gridExtra",
  "httr",
  "jsonlite",
  "mgsub",
  "patchwork",
  "plotly",
  "purrr",
  "RcppRoll",
  "RColorBrewer",
  "rstatix",
  "scales",
  "stringr",
  "tidyverse",
  "reshape2",
  "readxl",
  "zoo"
))
```

The following packages should be installed from GitHub using `devtools`:

```r
devtools::install_github("jweile/yogitools")
devtools::install_github("jweile/yogiroc")
```

---

## 🔹 FPocket

**Purpose:** Identify and evaluate ligand-binding pockets across MD snapshots and CPOX variants using [fpocket](https://github.com/Discngine/fpocket).

### Files & Steps:

* `Ref_Pocket1.txt`, `Ref_Pocket2.txt`: Lists of reference residues for pockets of interest.
* `GetReferencePoket_1.py`: Defines and validates pocket residues from initial structures.
* `prepareFpocket_2.py`: Extracts individual PDB frames from MD trajectories.
* `run_fpocket_3.sh`: Runs fpocket on each frame to detect binding pockets.
* `ScreenPocket_4.py`: Compares detected pockets to reference pockets based on residue overlap.
* `Pick_pocket_5.py`: Extracts physicochemical features, such as volume and polarity, for pockets of interest.

### Dependencies:

```bash
pip install MDAnalysis
pip install prodigy
```

Additional requirements:

* [fpocket](https://github.com/Discngine/fpocket) binary
* [PRODIGY](https://github.com/haddocking/prodigy) for optional pocket affinity prediction

---

## 🔹 Hinge_analysis

**Purpose:** Identify global hinge sites, which are key pivot points involved in collective protein motions, using normal mode analysis.

### Files:

* `CPOX_AF.pdb`: Reference AlphaFold structure of CPOX.
* `find_hinges.ipynb`: Builds the structural ensemble, performs GNM/ANM analysis, and detects hinge sites.

### Dependencies:

```bash
pip install prody numpy matplotlib
```

**Citation:**
Zhang H. et al., *Global hinge sites of proteins as target sites for drug binding*

---

## 🔹 MD_analysis

**Purpose:** Analyze molecular dynamics across AlphaFold-based and crystal-structure-based CPOX simulations.

### Subfolders:

* `AF_analysis/`

  * `calcDIstances.ipynb`: Calculates inter-residue distances across MD frames.
  * `MD_MSF.ipynb`: Computes mean square fluctuations (MSF).

* `Crystal_analysis/`

  * Mirror analysis structure for crystal-structure-based systems.

### Dependencies:

```bash
pip install MDAnalysis prody matplotlib pandas seaborn numpy
```

---

## 🔹 PCA_analysis

**Purpose:** Perform principal component analysis (PCA) to evaluate dominant protein motions and compare conformational sampling across CPOX variants and structural models. Prior to PCA, MD snapshots were structurally aligned using ProDy’s iterative superposition (iterpose) procedure, allowing WT and variant trajectories to be projected and compared within a common principal component space.

### Files:

* `EvalMD_PCA_crystal.ipynb`: PCA analysis for crystal-structure-based MD systems.
* `EvalMD_PCA_WT.ipynb`: PCA analysis for AlphaFold-based MD systems.
* `AF_plots/`: PCA plots from AlphaFold-based simulations.
* `Crystal_plots/`: PCA plots from crystal-structure-based simulations.

### Dependencies:

```bash
pip install MDAnalysis prody matplotlib pandas seaborn numpy
```

---

## 🔹 Docking_data

**Purpose:** Evaluate docking results of two ligands, **coproporphyrinogen III** and **uroporphyrinogen III**, to CPOX structures derived from AlphaFold and crystal models.

### Structure:

* `UroprophyrinogenIII.pdbqt`: Ligand structure used for docking.
* `CoproporphyrinogenIII.pdbqt`: Ligand structure used for docking.
* `Vina_job`: Shell script or command file used to run AutoDock Vina docking jobs.

### Subfolders:

* `Docking_AF/`: Docking results for AlphaFold-based structures.
* `Docking_crystal/`: Docking results for crystal-structure-based structures.

Each folder contains five CPOX system folders:

* `WT/`
* `G188Q/`
* `N272H/`
* `V135A/`
* `L155W/`

Each mutation folder contains docking outputs for MD snapshots from multiple frames. For each docking snapshot:

* One `.pdbqt` file corresponds to the protein structure used for that docking instance.
* Five replicate folders are included: `Run1/` through `Run5/`.

Each `RunX/` folder contains:

* `copro/`: Docking results for **coproporphyrinogen III**.
* `uro/`: Docking results for **uroporphyrinogen III**.

Inside each ligand folder:

* `CPOX_A.txt`: Docking parameters used.
* `CPOX_A.log`, `CPOX_A.dlg`: AutoDock Vina docking log files containing binding scores and docking modes.
* `.pdbqt`: Output docking conformations of the ligand.
* `.pse`: PyMOL session file for visualizing docking poses, if available.

### Dependencies:

* [AutoDock Vina](http://vina.scripps.edu/)
* Optional: [PyMOL](https://pymol.org/) for visualization of `.pse` files

---

## 🔹 prodigy-lig

**Purpose:** Estimate ligand-binding free energies from MD-derived CPOX structures using PRODIGY-LIG. These analyses were used to evaluate the binding of coproporphyrinogen III and uroporphyrinogen III across CPOX variants, simulation replicates, and MD frames.

### Method Summary:

Binding affinity was estimated using PRODIGY-LIG on ligand-bound MD trajectory frames. For each system, the ligand-bound chain and binding pose were selected from the AutoDock Vina docking results based on the consensus between the most favorable docking score and the highest active-site pocket occupancy. The selected docking-defined chain was then used consistently for PRODIGY-LIG analysis, generating a single time-dependent binding free energy profile, ΔG(t), for downstream analysis.

### Files & Steps:

* `write_frames.py`: First step. Uses `prmtop` and `dcd` trajectory files to write MD frames as PDB files.

* `rewrite_chains_all_frames.py`: Second step. Reads and rewrites the PDB files by renaming chain `X` to chain `A` and chain `B` for the CPOX dimer.

* `run_prodigy_lig_batch.py`: Third step. Runs PRODIGY-LIG in batch mode to calculate ligand-binding free energies between ligands and protein structures.

* `mergeDataAB.py`: Fourth step. Merges PRODIGY-LIG results from the two CPOX chains into one file.

* `merge_prodigy_results.py`: Fifth step. Collects merged chain files into one folder and combines all ligand-binding free-energy results across systems, mutations, and replicates.

* `Results_prodigy-lig.xlsx`: Processed PRODIGY-LIG results for MD frames. Free energies are reported from the PRODIGY-LIG method, with binding free energy evaluated for frames along the MD trajectories.

### Dependencies:

* PRODIGY-LIG
* Python packages commonly used in the MD analysis workflow, including:

```bash
pip install MDAnalysis pandas numpy openpyxl
```

---

## 🔹 Ori_data

**Purpose:** Store original and processed data tables used for downstream analysis of CPOX dynamics, pocket features, secondary structure, solvent accessibility, and model-specific comparisons.

### Files:

* `Mercury_SASA_all_cysteines_long.csv`: Solvent-accessible surface area data for all cysteine residues from all apo simulations based on the AlphaFold model.

* `allData_AF.xlsx`: Combined distance and fpocket data from simulations based on AlphaFold CPOX models.

* `allData_crystal.xlsx`: Combined distance and fpocket data from simulations based on crystal-structure CPOX models. This file has the same type of information as `allData_AF.xlsx`, but for crystal-structure-based simulations.

* `Secondary_structure_all.xlsx`: Secondary structure changes across different simulations.

### Method Summary:

MD snapshots were recorded every 100 ps during each simulation. ProDy was used to perform PCA after aligning WT and variant snapshots onto the starting structure, either the initial AlphaFold model or the crystal structure. Root mean square deviations (RMSDs) of MD snapshots were calculated relative to the reference structure, and residue mean square fluctuations (MSFs) were calculated for WT and each variant. Changes in secondary structural elements were analyzed using the VMD secondary structure evaluation module.

---

## 📚 Citations

* **PRODIGY**: [https://github.com/haddocking/prodigy](https://github.com/haddocking/prodigy-lig)
* **fpocket**: https://github.com/Discngine/fpocket
* **AutoDock Vina**: http://vina.scripps.edu/
* **Hinge site analysis**: Haotian Z. et al., *Global hinge sites of proteins as target sites for drug binding*

---

## 📬 Contact

For questions or collaboration inquiries, please contact:

**Haotian Zhang** — [haz100@pitt.edu](mailto:haz100@pitt.edu)
**Warren van Loggerenberg** — [WAV14@pitt.edu](mailto:WAV14@pitt.edu)
