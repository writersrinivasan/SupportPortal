#!/usr/bin/env python3

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Starting SupportPortal...")
    print("Python version:", sys.version)
    
    # Test imports
    print("Testing imports...")
    import flask
    print("✓ Flask imported successfully")
    
    from app import create_app
    print("✓ App module imported successfully")
    
    # Create and run the app
    app = create_app()
    print("✓ App created successfully")
    
    print("Starting server on http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
