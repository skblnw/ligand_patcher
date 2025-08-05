# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains CHARMM-GUI generated molecular dynamics simulation files for ligand patching and membrane protein simulations. The project includes two main simulation systems:

1. **ligand-charmm-gui-5442431562/**: Ligand modification and combination system
2. **system-charmm-gui-5442443097/**: Complete membrane protein system with equilibration and production runs

## Core Python Scripts

### Ligand Processing Scripts (ligand-charmm-gui-5442431562/)

- **combinePdb.py**: Combines multiple PDB chains with modified ligands
  - Usage: `python combinePdb.py -option [LoadPDBID|UploadPDB|combinatorial] -chains CHAIN_LIST -orig ORIGINAL_FILE -resn RESIDUE_NAME [-multi MULTI_CHAINS]`
  - Handles coordinate mapping between uploaded and original structures
  - Supports combinatorial ligand generation

- **multiGen.py**: Generates multiple ligand conformations and coordinate files  
  - Similar interface to combinePdb.py but focuses on multi-ligand systems
  - Creates `.crd` files for CHARMM input

- **gromacs/psf2itp_ligrm.py**: Converts PSF topology files to GROMACS ITP format

### System Analysis Scripts (system-charmm-gui-5442443097/)

- **pentest.py**: Comprehensive penetration testing for molecular systems
  - Detects lipid ring penetrations using least-squares plane fitting
  - Identifies protein surface penetrations using alpha-shape analysis  
  - Usage: `python pentest.py PSF_FILE CRD_FILE [-pbc A B] [-xtl rect|hexa] [-v] [-hull HULL_PATH]`
  - Requires Ken Clarkson's Hull program for alpha-shape calculations

- **findrings.py**: Ring detection and analysis utilities
- **checkfft.py**: FFT grid validation for CHARMM calculations  
- **addCrystPdb.py**: Crystal structure processing utilities

## GROMACS Simulation Workflow

The GROMACS directory contains a complete simulation pipeline:

### Running Simulations
```bash
cd system-charmm-gui-5442443097/gromacs/

# Minimization (use double precision if single precision fails)
gmx grompp -f step6.0_minimization.mdp -o step6.0_minimization.tpr -c step5_input.gro -r step5_input.gro -p topol.top -n index.ndx
gmx_d mdrun -v -deffnm step6.0_minimization

# Equilibration (6 steps)
gmx grompp -f step6.1_equilibration.mdp -o step6.1_equilibration.tpr -c step6.0_minimization.gro -r step5_input.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm step6.1_equilibration
# Continue for steps 6.2 through 6.6...

# Production runs (default 10 cycles)
gmx grompp -f step7_production.mdp -o step7_1.tpr -c step6.6_equilibration.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm step7_1
```

### MPI Parallelization
For parallel runs: `mpirun -np $NUM_CPU gmx mdrun -ntomp 1`

## Key File Formats

- **YAML Configuration**: `ligandrm.yml`, `header.yml`, `glycan.yml` contain simulation metadata
- **CHARMM Files**: `.psf` (topology), `.crd` (coordinates), `.str` (parameters)
- **GROMACS Files**: `.gro` (coordinates), `.top` (topology), `.mdp` (simulation parameters)
- **PDB Files**: Protein structures with various naming conventions (`*_modified.pdb`, `*_heta.pdb`, etc.)

## Force Field Parameters

Located in `toppar/` directories:
- CHARMM36 parameter files (`.prm`) and topology files (`.rtf`)
- Specialized parameters for lipids, proteins, carbohydrates, and ligands
- Custom force field modifications in `.str` files

## System Requirements

- Python 2/3 with numpy, networkx, yaml packages
- GROMACS 2019.2 or higher (Verlet cutoff scheme)
- Ken Clarkson's Hull program for alpha-shape analysis (pentest.py)
- CHARMM for coordinate and parameter file generation