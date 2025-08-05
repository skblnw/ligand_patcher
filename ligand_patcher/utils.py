"""Utility functions for ligand patcher."""

import os
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:
    # Fallback for simple YAML parsing if PyYAML not available
    class SimpleYAML:
        @staticmethod
        def safe_load(stream):
            """Simple YAML parser for basic key: value pairs."""
            data = {}
            for line in stream:
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
            return data
    yaml = SimpleYAML()


def backup_file(filepath, backup_suffix=".backup"):
    """Create a backup copy of a file."""
    backup_path = str(filepath) + backup_suffix
    if os.path.exists(filepath) and not os.path.exists(backup_path):
        shutil.copy2(filepath, backup_path)
        return backup_path
    return None


def read_yaml_file(filepath):
    """Read and parse a YAML file."""
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"Error reading YAML file {filepath}: {e}")


def parse_gro_header(gro_file):
    """Parse the header of a GRO file to get atom count."""
    with open(gro_file, 'r') as f:
        title = f.readline().strip()
        atom_count = int(f.readline().strip())
    return title, atom_count


def update_gro_header(gro_file, new_atom_count):
    """Update the atom count in a GRO file header."""
    with open(gro_file, 'r') as f:
        lines = f.readlines()
    
    lines[1] = f"{new_atom_count:5d}\n"
    
    with open(gro_file, 'w') as f:
        f.writelines(lines)


def get_ligand_name_from_yml(yml_file):
    """Extract ligand residue name from YAML metadata."""
    data = read_yaml_file(yml_file)
    if 'newresn' in data:
        return data['newresn']
    elif 'orgresn' in data:
        return data['orgresn'] 
    else:
        raise ValueError(f"Could not find residue name in {yml_file}")


def find_ligand_itp_file(ligand_dir):
    """Find the ligand ITP file in the ligand directory."""
    gromacs_dir = os.path.join(ligand_dir, 'gromacs')
    if not os.path.exists(gromacs_dir):
        raise FileNotFoundError(f"GROMACS directory not found in {ligand_dir}")
    
    # Look for ITP files
    itp_files = [f for f in os.listdir(gromacs_dir) if f.endswith('.itp')]
    if not itp_files:
        raise FileNotFoundError(f"No ITP files found in {gromacs_dir}")
    
    # Filter out common force field files and prefer ligand-specific ITP
    force_field_files = ['charmm36.itp', 'forcefield.itp', 'atomtypes.itp']
    ligand_itp_files = [f for f in itp_files if f not in force_field_files]
    
    if ligand_itp_files:
        # Return the first ligand-specific ITP file
        return os.path.join(gromacs_dir, ligand_itp_files[0])
    else:
        # Fall back to first ITP file if no ligand-specific found
        return os.path.join(gromacs_dir, itp_files[0])


def validate_system_directory(system_dir):
    """Validate that system directory contains required files."""
    required_files = [
        'gromacs/step5_input.gro',
        'gromacs/topol.top',
        'gromacs/index.ndx'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(system_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        raise FileNotFoundError(f"Missing required files in {system_dir}: {missing_files}")


def validate_ligand_directory(ligand_dir):
    """Validate that ligand directory contains required files."""
    required_files = [
        'ligandrm.pdb',
        'ligandrm.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(ligand_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        raise FileNotFoundError(f"Missing required files in {ligand_dir}: {missing_files}")
    
    # Also check for ITP file
    try:
        find_ligand_itp_file(ligand_dir)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ligand ITP file validation failed: {e}")


def pdb_to_gro_line(pdb_line, atom_number, residue_number):
    """Convert a PDB ATOM line to GRO format."""
    # Parse PDB line
    atom_name = pdb_line[12:16].strip()
    res_name = pdb_line[17:20].strip()
    x = float(pdb_line[30:38]) / 10.0  # Convert Å to nm
    y = float(pdb_line[38:46]) / 10.0
    z = float(pdb_line[46:54]) / 10.0
    
    # Format as GRO line: residue_num + residue_name + atom_name + atom_num + x + y + z
    gro_line = f"{residue_number:5d}{res_name:<5s}{atom_name:>5s}{atom_number:5d}{x:8.3f}{y:8.3f}{z:8.3f}\n"
    return gro_line


def get_equilibration_mdp_files(system_dir):
    """Get list of equilibration MDP files in the system directory."""
    gromacs_dir = os.path.join(system_dir, 'gromacs')
    mdp_files = []
    
    # Look for step6.X_equilibration.mdp files
    for i in range(1, 10):  # step6.1 through step6.9
        mdp_file = os.path.join(gromacs_dir, f'step6.{i}_equilibration.mdp')
        if os.path.exists(mdp_file):
            mdp_files.append(mdp_file)
    
    return mdp_files