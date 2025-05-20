"""Main module for MicroGenesis application."""

import argparse
from microgenesis.example import Example

def main():
    """Run the main application with command line arguments."""
    parser = argparse.ArgumentParser(
        description="MicroGenesis - A Python project template"
    )
    parser.add_argument(
        "--name", 
        type=str, 
        default="World", 
        help="Name to greet (default: %(default)s)"
    )
    parser.add_argument(
        "--version", 
        action="store_true",
        help="Show version information and exit"
    )
    
    args = parser.parse_args()
    
    if args.version:
        from microgenesis import __version__
        print(f"MicroGenesis version {__version__}")
        return
        
    example = Example(name=args.name)
    print(example.greet())
    
if __name__ == "__main__":
    main()
