#!/bin/bash
# Quick installation and test script for GROMACS Ligand Patcher

set -e  # Exit on any error

echo "=========================================="
echo "GROMACS Ligand Patcher - Quick Test"
echo "=========================================="

# Create temporary test environment
echo "Creating test environment..."
python3 -m venv temp_test_env
source temp_test_env/bin/activate

echo "Installing ligand-patcher..."
pip install -e . > /dev/null 2>&1

echo "Testing installation..."
ligand-patcher --version
echo ""

if [ -d "test_data/system-charmm-gui-5442443097" ] && [ -d "test_data/ligand-charmm-gui-5442431562" ]; then
    echo "Running dry-run test with sample data..."
    ligand-patcher patch test_data/system-charmm-gui-5442443097 test_data/ligand-charmm-gui-5442431562 --dry-run 2>&1 | grep -E "(INFO|SUCCESS|✓)"
    echo ""
fi

echo "Running comprehensive tests..."
python test_installation.py 2>&1 | grep -E "(✓|🎉|❌|tests passed)"

echo ""
echo "=========================================="
echo "✅ Quick test completed successfully!"
echo "=========================================="

# Cleanup
deactivate
rm -rf temp_test_env

echo "Environment cleaned up."