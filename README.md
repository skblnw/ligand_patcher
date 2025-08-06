# GROMACS Ligand Patcher

A Python tool to patch CHARMM-GUI generated membrane protein systems by integrating ligands for GROMACS molecular dynamics simulations.

## Overview

This tool simplifies the process of adding ligands to CHARMM-GUI generated membrane protein systems. It handles:

1. **Coordinate Integration**: Adds ligand coordinates to the system
2. **Topology Updates**: Integrates ligand topology and parameters  
3. **Restraint Setup**: Configures ligand restraints for equilibration

## Features

- Direct coordinate insertion from ligand PDB to system GRO files
- Automatic topology file updates and molecule counting
- Equilibration restraint configuration for ligands
- Simple command-line interface
- Preserves original CHARMM-GUI file structure

## Installation

### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/ligand-patcher.git
cd ligand-patcher

# Create and activate conda environment
conda env create -f environment.yml
conda activate ligand-patcher

# Verify installation
ligand-patcher --version
```

### Option 2: Using Python venv

```bash
# Clone the repository
git clone https://github.com/yourusername/ligand-patcher.git
cd ligand-patcher

# Create and activate virtual environment
python -m venv ligand-patcher-env
source ligand-patcher-env/bin/activate  # On Windows: ligand-patcher-env\Scripts\activate

# Install the package
pip install -e .

# Verify installation
ligand-patcher --version
```

### Option 3: Direct pip install

```bash
git clone https://github.com/yourusername/ligand-patcher.git
cd ligand-patcher
pip install -e .
```

### Testing Installation

After installation, verify everything works correctly:

```bash
# Test the CLI
ligand-patcher --version
ligand-patcher --help

# Run comprehensive installation tests
python test_installation.py

# Test with your own data (dry run)
ligand-patcher patch your-system-dir your-ligand-dir --dry-run --verbose
```

## Usage

### Basic Usage
```bash
ligand-patcher patch system-charmm-gui-123 ligand-charmm-gui-456
```

### With Output Directory
```bash
ligand-patcher patch system-dir ligand-dir --output patched-system
```

### Dry Run
```bash
ligand-patcher patch system-dir ligand-dir --dry-run
```

## Input Requirements

### System Directory (system-charmm-gui-xxx)
- `gromacs/step5_input.gro` - System coordinates
- `gromacs/topol.top` - System topology
- `gromacs/step6.X_equilibration.mdp` - Equilibration parameters
- `gromacs/index.ndx` - Atom groups

### Ligand Directory (ligand-charmm-gui-xxx)  
- `ligandrm.pdb` - Ligand coordinates
- `gromacs/LIGAND.itp` - Ligand topology
- `ligandrm.yml` - Ligand metadata

## Output

The tool creates a patched system with:
- Updated coordinate file with ligand atoms
- Modified topology including ligand parameters
- Equilibration files configured with ligand restraints
- Backup copies of original files

## Requirements

- Python 3.6+
- GROMACS (for running simulations)
- Standard library only (no external dependencies)

## License

MIT License - see LICENSE file for details.

## Contributing  

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please use the GitHub issue tracker.

## Acknowledgement

Xi'an Jiaotong-Liverpool University (XJTLU) Summer Undergraduate Research Fellowship (SURF) code:1335,1415

Initiates: TXY
