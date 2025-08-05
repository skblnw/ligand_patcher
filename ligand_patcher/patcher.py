"""Main LigandPatcher class for integrating ligands into CHARMM-GUI systems."""

import os
import shutil
import logging
from pathlib import Path

from .utils import (
    backup_file, validate_system_directory, validate_ligand_directory,
    parse_gro_header, update_gro_header, get_ligand_name_from_yml,
    find_ligand_itp_file, pdb_to_gro_line, get_equilibration_mdp_files
)


class LigandPatcher:
    """Main class for patching CHARMM-GUI systems with ligands."""
    
    def __init__(self, system_dir, ligand_dir, output_dir=None, dry_run=False):
        """
        Initialize LigandPatcher.
        
        Args:
            system_dir (str): Path to system-charmm-gui-xxx directory
            ligand_dir (str): Path to ligand-charmm-gui-xxx directory  
            output_dir (str, optional): Output directory. Defaults to system_dir.
            dry_run (bool): If True, only show what would be done without making changes
        """
        self.system_dir = Path(system_dir)
        self.ligand_dir = Path(ligand_dir)
        self.output_dir = Path(output_dir) if output_dir else self.system_dir
        self.dry_run = dry_run
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize file paths
        self._setup_file_paths()
        
        # Validate input directories
        self._validate_inputs()
    
    def _setup_file_paths(self):
        """Set up all file paths used by the patcher."""
        # System files
        self.system_gro = self.system_dir / 'gromacs/step5_input.gro'
        self.system_top = self.system_dir / 'gromacs/topol.top'
        self.system_ndx = self.system_dir / 'gromacs/index.ndx'
        
        # Ligand files
        self.ligand_pdb = self.ligand_dir / 'ligandrm.pdb'
        self.ligand_yml = self.ligand_dir / 'ligandrm.yml'
        
        # Output files (if different from system_dir)
        if self.output_dir != self.system_dir:
            self.output_gro = self.output_dir / 'gromacs/step5_input.gro'
            self.output_top = self.output_dir / 'gromacs/topol.top'
            self.output_ndx = self.output_dir / 'gromacs/index.ndx'
        else:
            self.output_gro = self.system_gro
            self.output_top = self.system_top
            self.output_ndx = self.system_ndx
    
    def _validate_inputs(self):
        """Validate input directories and files."""
        self.logger.info("Validating input directories...")
        validate_system_directory(str(self.system_dir))
        validate_ligand_directory(str(self.ligand_dir))
        self.logger.info("Input validation successful")
    
    def patch(self):
        """
        Main patching workflow.
        
        Performs all three steps:
        1. Add ligand coordinates
        2. Update topology 
        3. Update restraints
        """
        self.logger.info("Starting ligand patching process...")
        
        if self.dry_run:
            self.logger.info("DRY RUN MODE - No files will be modified")
        
        # Copy system to output directory if needed
        if self.output_dir != self.system_dir:
            self._copy_system_to_output()
        
        # Step 1: Add ligand coordinates
        self.add_ligand_coordinates()
        
        # Step 2: Update topology
        self.update_topology()
        
        # Step 3: Update restraints
        self.update_restraints()
        
        self.logger.info("Ligand patching completed successfully!")
    
    def _copy_system_to_output(self):
        """Copy system directory to output directory."""
        if self.dry_run:
            self.logger.info(f"Would copy {self.system_dir} to {self.output_dir}")
            return
        
        self.logger.info(f"Copying system to output directory: {self.output_dir}")
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        shutil.copytree(self.system_dir, self.output_dir)
    
    def add_ligand_coordinates(self):
        """Step 1: Add ligand coordinates to the system GRO file."""
        self.logger.info("Step 1: Adding ligand coordinates...")
        
        # Parse ligand PDB to extract coordinates
        ligand_atoms = self._parse_ligand_pdb()
        
        # Get current system info
        title, current_atom_count = parse_gro_header(str(self.output_gro))
        
        # Calculate new atom count
        new_atom_count = current_atom_count + len(ligand_atoms)
        
        if self.dry_run:
            self.logger.info(f"Would add {len(ligand_atoms)} ligand atoms to {self.output_gro}")
            self.logger.info(f"Would update atom count from {current_atom_count} to {new_atom_count}")
            return
        
        # Backup original file
        backup_file(str(self.output_gro))
        
        # Read existing GRO file
        with open(self.output_gro, 'r') as f:
            lines = f.readlines()
        
        # Find insertion point (before box vectors)
        box_line_idx = len(lines) - 1
        
        # Insert ligand atoms
        ligand_lines = []
        atom_number = current_atom_count + 1
        residue_number = self._get_next_residue_number(lines)
        
        for pdb_line in ligand_atoms:
            gro_line = pdb_to_gro_line(pdb_line, atom_number, residue_number)
            ligand_lines.append(gro_line)
            atom_number += 1
        
        # Insert ligand lines before box vectors
        lines = lines[:box_line_idx] + ligand_lines + [lines[box_line_idx]]
        
        # Update atom count in header
        lines[1] = f"{new_atom_count:5d}\n"
        
        # Write updated file
        with open(self.output_gro, 'w') as f:
            f.writelines(lines)
        
        self.logger.info(f"Added {len(ligand_atoms)} ligand atoms to {self.output_gro}")
    
    def _parse_ligand_pdb(self):
        """Parse ligand PDB file to extract ATOM lines."""
        ligand_atoms = []
        with open(self.ligand_pdb, 'r') as f:
            for line in f:
                if line.startswith('ATOM'):
                    ligand_atoms.append(line.strip())
        
        if not ligand_atoms:
            raise ValueError(f"No ATOM records found in {self.ligand_pdb}")
        
        return ligand_atoms
    
    def _get_next_residue_number(self, gro_lines):
        """Get the next available residue number from GRO file."""
        max_res_num = 0
        for line in gro_lines[2:-1]:  # Skip header and box line
            if len(line.strip()) > 0:
                try:
                    res_num = int(line[:5])
                    max_res_num = max(max_res_num, res_num)
                except ValueError:
                    continue
        return max_res_num + 1
    
    def update_topology(self):
        """Step 2: Update topology files to include ligand."""
        self.logger.info("Step 2: Updating topology...")
        
        # Get ligand information
        ligand_name = get_ligand_name_from_yml(str(self.ligand_yml))
        ligand_itp = find_ligand_itp_file(str(self.ligand_dir))
        
        if self.dry_run:
            self.logger.info(f"Would add ligand '{ligand_name}' to topology")
            self.logger.info(f"Would copy {ligand_itp} to system toppar directory")
            return
        
        # Copy ligand ITP file to system
        self._copy_ligand_itp(ligand_itp, ligand_name)
        
        # Update topology file
        self._update_topology_file(ligand_name)
        
        self.logger.info(f"Updated topology for ligand '{ligand_name}'")
    
    def _copy_ligand_itp(self, ligand_itp, ligand_name):
        """Copy ligand ITP file to system toppar directory."""
        toppar_dir = self.output_dir / 'gromacs/toppar'
        toppar_dir.mkdir(exist_ok=True)
        
        # Use ligand name for ITP file
        target_itp = toppar_dir / f'{ligand_name}.itp'
        shutil.copy2(ligand_itp, target_itp)
        
        self.logger.info(f"Copied {ligand_itp} to {target_itp}")
    
    def _update_topology_file(self, ligand_name):
        """Update main topology file to include ligand."""
        # Backup original file
        backup_file(str(self.output_top))
        
        with open(self.output_top, 'r') as f:
            lines = f.readlines()
        
        # Find insertion points
        include_idx = None
        molecules_idx = None
        
        for i, line in enumerate(lines):
            if line.startswith('#include') and 'TIP3.itp' in line:
                include_idx = i + 1
            elif line.strip() == '[ molecules ]':
                molecules_idx = i
                break
        
        if include_idx is None:
            raise ValueError("Could not find insertion point for include statement")
        if molecules_idx is None:
            raise ValueError("Could not find [molecules] section")
        
        # Add include statement
        include_line = f'#include "toppar/{ligand_name}.itp"\n'
        lines.insert(include_idx, include_line)
        
        # Add molecule to [molecules] section (after updating indices)
        molecules_idx += 1  # Account for inserted include line
        
        # Find end of molecules section
        end_idx = len(lines)
        for i in range(molecules_idx + 2, len(lines)):  # Skip header and comment
            if lines[i].strip() == '' or lines[i].startswith('['):
                end_idx = i
                break
        
        # Insert ligand molecule entry
        ligand_molecule_line = f'{ligand_name}   \t           1\n'
        lines.insert(end_idx, ligand_molecule_line)
        
        # Write updated file
        with open(self.output_top, 'w') as f:
            f.writelines(lines)
    
    def update_restraints(self):
        """Step 3: Update restraints for ligand during equilibration."""
        self.logger.info("Step 3: Updating restraints...")
        
        # Get ligand name
        ligand_name = get_ligand_name_from_yml(str(self.ligand_yml))
        
        # Get equilibration MDP files
        mdp_files = get_equilibration_mdp_files(str(self.output_dir))
        
        if not mdp_files:
            self.logger.warning("No equilibration MDP files found")
            return
        
        if self.dry_run:
            self.logger.info(f"Would update {len(mdp_files)} equilibration MDP files")
            self.logger.info(f"Would add ligand restraints for '{ligand_name}'")
            return
        
        # Update each MDP file
        for mdp_file in mdp_files:
            self._update_mdp_restraints(mdp_file, ligand_name)
        
        # Update index file to include ligand in SOLU group
        self._update_index_file(ligand_name)
        
        self.logger.info(f"Updated restraints for {len(mdp_files)} equilibration files")
    
    def _update_mdp_restraints(self, mdp_file, ligand_name):
        """Update a single MDP file to include ligand restraints."""
        # Backup original file
        backup_file(mdp_file)
        
        with open(mdp_file, 'r') as f:
            lines = f.readlines()
        
        # Find and update define line
        for i, line in enumerate(lines):
            if line.startswith('define'):
                # Add ligand restraint to existing defines
                if '-DPOSRES_LIGAND' not in line:  
                    # Remove newline, add ligand restraint, add newline back
                    lines[i] = line.rstrip() + f' -DPOSRES_LIGAND -DPOSRES_FC_LIGAND=1000.0\n'
                break
        
        # Write updated file
        with open(mdp_file, 'w') as f:
            f.writelines(lines)
    
    def _update_index_file(self, ligand_name):
        """Update index file to include ligand atoms in SOLU group."""
        if not self.output_ndx.exists():
            self.logger.warning("Index file not found, skipping index update")
            return
        
        # For now, just log that this would be updated
        # Full implementation would parse index file and add ligand atoms to SOLU group
        self.logger.info(f"Index file update needed for ligand '{ligand_name}' (manual step required)")
        self.logger.info("Add ligand atoms to [ SOLU ] group in index.ndx manually")