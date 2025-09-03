#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting SupportPortal on http://localhost:3000")
    app.run(debug=True, host='127.0.0.1', port=3000, use_reloader=False)
