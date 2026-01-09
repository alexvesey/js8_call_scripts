#!/bin/bash
if [ ! -d ".venv" ]; then
    echo "Error: .venv does not exist in the current directory. Follow 'Venv Setup Instructions' in the README."
    exit 1
fi
source .venv/bin/activate
python3 js8.py --std
