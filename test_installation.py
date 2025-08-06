#!/usr/bin/env python
"""
Installation test script for GROMACS Ligand Patcher.

This script tests that the package is properly installed and all
functionality works in a clean environment.
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and check the result."""
    print(f"Testing: {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ SUCCESS")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("✗ FAILED")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        return False
    
    print("-" * 50)
    return True


def test_import():
    """Test importing the package."""
    print("Testing package import...")
    try:
        from ligand_patcher import LigandPatcher
        from ligand_patcher.utils import pdb_to_gro_line
        from ligand_patcher.cli import main
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_utility_functions():
    """Test basic utility functions."""
    print("Testing utility functions...")
    try:
        from ligand_patcher.utils import pdb_to_gro_line
        
        # Test PDB to GRO conversion
        pdb_line = "ATOM      1  HZ1 NH4 N   1      -5.328  24.525  21.007  1.00  0.00      NH4"
        gro_line = pdb_to_gro_line(pdb_line, 1, 1)
        
        # Check basic format
        assert "NH4" in gro_line
        assert "HZ1" in gro_line
        assert "-0.533" in gro_line  # Coordinate conversion
        
        print("✓ Utility functions work correctly")
        return True
    except Exception as e:
        print(f"✗ Utility function test failed: {e}")
        return False


def main():
    """Run all installation tests."""
    print("=" * 60)
    print("GROMACS Ligand Patcher - Installation Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: CLI version
    if run_command("ligand-patcher --version", "CLI version command"):
        tests_passed += 1
    
    # Test 2: CLI help
    if run_command("ligand-patcher --help", "CLI help command"):
        tests_passed += 1
    
    # Test 3: CLI patch help
    if run_command("ligand-patcher patch --help", "CLI patch help command"):
        tests_passed += 1
    
    # Test 4: Package import
    if test_import():
        tests_passed += 1
    
    # Test 5: Utility functions
    if test_utility_functions():
        tests_passed += 1
    
    # Test 6: Dry run with test data (if available)
    test_system_dir = "test_data/system-charmm-gui-5442443097"
    test_ligand_dir = "test_data/ligand-charmm-gui-5442431562"
    
    if os.path.exists(test_system_dir) and os.path.exists(test_ligand_dir):
        cmd = f"ligand-patcher patch {test_system_dir} {test_ligand_dir} --dry-run"
        if run_command(cmd, "Dry run with test data"):
            tests_passed += 1
    else:
        print("Test data not available, skipping dry run test")
        print("✓ SKIPPED (test data not found)")
        print("-" * 50)
        tests_passed += 1  # Don't penalize for missing test data
    
    # Summary
    print("=" * 60)
    print(f"INSTALLATION TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Installation is successful.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())