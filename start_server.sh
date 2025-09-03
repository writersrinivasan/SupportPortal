#!/bin/bash
cd /Users/srinivasanramanujam/CloneServicenow/SupportPortal
echo "Starting SupportPortal..."
echo "Working directory: $(pwd)"
echo "Python path: /Users/srinivasanramanujam/CloneServicenow/.venv/bin/python"

# Make the script executable and run it
chmod +x debug_run.py
/Users/srinivasanramanujam/CloneServicenow/.venv/bin/python debug_run.py
