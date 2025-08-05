"""Command-line interface for GROMACS Ligand Patcher."""

import argparse
import sys
import logging
from pathlib import Path

from .patcher import LigandPatcher
from . import __version__


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='ligand-patcher',
        description='Patch CHARMM-GUI membrane protein systems with ligands for GROMACS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage
  ligand-patcher patch system-charmm-gui-123 ligand-charmm-gui-456
  
  # With output directory  
  ligand-patcher patch system-dir ligand-dir --output patched-system
  
  # Dry run to see changes
  ligand-patcher patch system-dir ligand-dir --dry-run
  
  # Verbose output
  ligand-patcher patch system-dir ligand-dir --verbose
        '''
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Patch command
    patch_parser = subparsers.add_parser(
        'patch',
        help='Patch a system with a ligand',
        description='Integrate a ligand into a CHARMM-GUI membrane protein system'
    )
    
    patch_parser.add_argument(
        'system_dir',
        help='Path to system-charmm-gui-xxx directory',
        type=str
    )
    
    patch_parser.add_argument(
        'ligand_dir', 
        help='Path to ligand-charmm-gui-xxx directory',
        type=str
    )
    
    patch_parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        help='Output directory (default: modify system_dir in place)',
        type=str,
        default=None
    )
    
    patch_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    patch_parser.add_argument(
        '-v', '--verbose',
        action='store_true', 
        help='Enable verbose output'
    )
    
    patch_parser.add_argument(
        '--backup-suffix',
        default='.backup',
        help='Suffix for backup files (default: .backup)'
    )
    
    return parser


def setup_logging(verbose=False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def validate_directories(system_dir, ligand_dir):
    """Validate input directories exist."""
    system_path = Path(system_dir)
    ligand_path = Path(ligand_dir)
    
    if not system_path.exists():
        print(f"Error: System directory does not exist: {system_dir}", file=sys.stderr)
        return False
        
    if not system_path.is_dir():
        print(f"Error: System path is not a directory: {system_dir}", file=sys.stderr)
        return False
        
    if not ligand_path.exists():
        print(f"Error: Ligand directory does not exist: {ligand_dir}", file=sys.stderr)
        return False
        
    if not ligand_path.is_dir():
        print(f"Error: Ligand path is not a directory: {ligand_dir}", file=sys.stderr)
        return False
    
    return True


def cmd_patch(args):
    """Handle the patch command."""
    # Validate input directories exist
    if not validate_directories(args.system_dir, args.ligand_dir):
        return 1
    
    # Set up logging
    setup_logging(args.verbose)
    
    try:
        # Create patcher instance
        patcher = LigandPatcher(
            system_dir=args.system_dir,
            ligand_dir=args.ligand_dir,
            output_dir=args.output_dir,
            dry_run=args.dry_run
        )
        
        # Run patching process
        patcher.patch()
        
        if args.dry_run:
            print("\nDry run completed successfully!")
            print("Run without --dry-run to apply changes.")
        else:
            print("\nPatching completed successfully!")
            if args.output_dir:
                print(f"Patched system saved to: {args.output_dir}")
            else:
                print(f"System patched in place: {args.system_dir}")
                print("Original files backed up with .backup suffix")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logging.exception("Unexpected error occurred")
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'patch':
        return cmd_patch(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())