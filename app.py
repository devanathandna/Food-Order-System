"""
Baratie Backend Server - Entry Point for Render Deployment
This file allows Render to run the backend with: python app.py
"""

from backend.app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🍽️  Baratie Backend Server starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
