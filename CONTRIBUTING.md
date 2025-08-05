# Contributing to GROMACS Ligand Patcher

Thank you for your interest in contributing to the GROMACS Ligand Patcher! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ligand-patcher.git
   cd ligand-patcher
   ```

2. **Install in development mode**
   ```bash
   pip install -e .
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
# Run basic tests
python tests/test_patcher.py

# With pytest (if installed)
pytest tests/

# Run example
python examples/usage_example.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and modular

## Testing

- Add tests for new functionality
- Test with real CHARMM-GUI data when possible
- Use dry-run mode for testing to avoid file modifications
- Ensure backward compatibility

## Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, concise commit messages
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   ligand-patcher patch test-system test-ligand --dry-run
   ```

5. **Submit a pull request**
   - Describe the changes made
   - Include test results
   - Reference any related issues

## Reporting Issues

When reporting issues, please include:

- Version of ligand-patcher
- Python version and OS
- CHARMM-GUI system and ligand directory structure
- Complete error message and traceback
- Steps to reproduce the issue

## Feature Requests

Feature requests are welcome! Please:

- Check existing issues first
- Describe the use case clearly
- Explain why the feature would be useful
- Provide examples if possible

## Code Organization

```
ligand_patcher/
├── __init__.py          # Package initialization
├── cli.py              # Command-line interface
├── patcher.py          # Main LigandPatcher class
└── utils.py            # Utility functions
```

## Key Principles

1. **Simplicity**: Keep the tool focused and easy to use
2. **Reliability**: Extensive validation and error handling
3. **Compatibility**: Work with standard CHARMM-GUI outputs
4. **Safety**: Always backup original files
5. **Transparency**: Clear logging and dry-run capabilities

## Questions?

Feel free to open an issue for questions or discussion about contributing to the project.