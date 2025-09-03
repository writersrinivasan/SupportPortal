#!/usr/bin/env python3
"""
SupportPortal - A Flask-based ticketing system
Alternative runner with comprehensive error handling
"""

import sys
import os
import traceback
from pathlib import Path

def main():
    try:
        # Get the directory of this script
        script_dir = Path(__file__).parent.absolute()
        
        # Add to Python path
        sys.path.insert(0, str(script_dir))
        
        print(f"SupportPortal Starting...")
        print(f"Script directory: {script_dir}")
        print(f"Python executable: {sys.executable}")
        print(f"Python version: {sys.version}")
        
        # Check if we're in the right directory
        if not (script_dir / 'app').exists():
            print(f"ERROR: 'app' directory not found in {script_dir}")
            return False
            
        if not (script_dir / 'config.py').exists():
            print(f"ERROR: 'config.py' not found in {script_dir}")
            return False
        
        print("✓ Project structure verified")
        
        # Test imports step by step
        print("Testing imports...")
        
        import flask
        print(f"✓ Flask {flask.__version__} imported")
        
        import flask_sqlalchemy
        print(f"✓ Flask-SQLAlchemy imported")
        
        import flask_login
        print(f"✓ Flask-Login imported")
        
        # Change to project directory
        os.chdir(script_dir)
        print(f"✓ Working directory: {os.getcwd()}")
        
        # Import our app
        from app import create_app
        print("✓ App module imported successfully")
        
        # Create the Flask app
        app = create_app()
        print("✓ Flask app created successfully")
        
        # Start the server
        print("\n" + "="*50)
        print("🚀 SupportPortal is starting...")
        print("📍 URL: http://localhost:8080")
        print("🛑 Press CTRL+C to stop")
        print("="*50 + "\n")
        
        app.run(
            debug=True,
            host='127.0.0.1',
            port=8080,
            use_reloader=False,
            threaded=True
        )
        
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print("\nThis might be due to missing dependencies.")
        print("Try running: pip install -r requirements.txt")
        traceback.print_exc()
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
