#!/usr/bin/env python
"""Setup script for GROMACS Ligand Patcher."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ligand-patcher",
    version="1.0.0",
    author="GROMACS MD Expert",
    author_email="expert@example.com",
    description="A tool to patch CHARMM-GUI membrane protein systems with ligands for GROMACS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ligand-patcher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Keeping minimal - only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "ligand-patcher=ligand_patcher.cli:main",
        ],
    },
    keywords="gromacs charmm-gui molecular dynamics ligand membrane protein",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ligand-patcher/issues",
        "Source": "https://github.com/yourusername/ligand-patcher",
        "Documentation": "https://github.com/yourusername/ligand-patcher#readme",
    },
)