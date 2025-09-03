#!/usr/bin/env python3
import sys
import os

print("=== Minimal Flask Test ===")
print(f"Python: {sys.executable}")
print(f"Working dir: {os.getcwd()}")

try:
    import flask
    print(f"✓ Flask {flask.__version__} OK")
    
    app = flask.Flask(__name__)
    
    @app.route('/')
    def hello():
        return '<h1>SupportPortal Test - Server is Working!</h1><p>If you see this, the server is running correctly.</p>'
    
    print("✓ Simple Flask app created")
    print("🚀 Starting test server on http://localhost:3000")
    print("Press Ctrl+C to stop")
    
    app.run(host='127.0.0.1', port=3000, debug=False)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
