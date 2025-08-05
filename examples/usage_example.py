#!/usr/bin/env python
"""
Example usage of the GROMACS Ligand Patcher.

This script demonstrates how to use the LigandPatcher class programmatically
to integrate ligands into CHARMM-GUI membrane protein systems.
"""

import sys
from pathlib import Path

# Add the parent directory to Python path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

from ligand_patcher import LigandPatcher


def example_basic_usage():
    """Example of basic ligand patching."""
    print("=== Basic Usage Example ===")
    
    # Define directories
    system_dir = "system-charmm-gui-5442443097"
    ligand_dir = "ligand-charmm-gui-5442431562" 
    
    try:
        # Create patcher instance
        patcher = LigandPatcher(
            system_dir=system_dir,
            ligand_dir=ligand_dir,
            dry_run=True  # Use dry run for this example
        )
        
        # Run the patching process
        patcher.patch()
        
        print("✓ Dry run completed successfully!")
        print("Remove dry_run=True to apply changes.")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def example_with_output_directory():
    """Example using a separate output directory."""
    print("\n=== Output Directory Example ===")
    
    system_dir = "system-charmm-gui-5442443097"
    ligand_dir = "ligand-charmm-gui-5442431562"
    output_dir = "patched_system"
    
    try:
        # Create patcher with output directory
        patcher = LigandPatcher(
            system_dir=system_dir,
            ligand_dir=ligand_dir,
            output_dir=output_dir,
            dry_run=True
        )
        
        patcher.patch()
        
        print(f"✓ Would create patched system in: {output_dir}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def example_step_by_step():
    """Example of running individual steps."""
    print("\n=== Step-by-Step Example ===")
    
    system_dir = "system-charmm-gui-5442443097"
    ligand_dir = "ligand-charmm-gui-5442431562"
    
    try:
        patcher = LigandPatcher(
            system_dir=system_dir,
            ligand_dir=ligand_dir,
            dry_run=True
        )
        
        print("Step 1: Adding ligand coordinates...")
        patcher.add_ligand_coordinates()
        
        print("Step 2: Updating topology...")
        patcher.update_topology()
        
        print("Step 3: Updating restraints...")
        patcher.update_restraints()
        
        print("✓ All steps completed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def example_error_handling():
    """Example of error handling."""
    print("\n=== Error Handling Example ===")
    
    # Try with non-existent directories
    try:
        patcher = LigandPatcher(
            system_dir="nonexistent_system",
            ligand_dir="nonexistent_ligand",
            dry_run=True
        )
        patcher.patch()
        
    except FileNotFoundError as e:
        print(f"✓ Caught expected error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    """Run all examples."""
    print("GROMACS Ligand Patcher - Usage Examples")
    print("=" * 50)
    
    example_basic_usage()
    example_with_output_directory()
    example_step_by_step()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use with real data:")
    print("1. Replace directory names with your actual CHARMM-GUI directories")
    print("2. Remove dry_run=True to apply changes")
    print("3. Check output for any warnings or manual steps required")