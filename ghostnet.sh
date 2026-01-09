#!/bin/bash
if [ ! -d ".venv" ]; then
    echo "Error: .venv does not exist in the current directory. Follow 'Venv Setup Instructions' in the README."
    exit 1
fi
# Source the virtual environment
source .venv/bin/activate

# Run your python script
python3 js8.py --gn
