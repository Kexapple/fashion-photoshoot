"""
Vercel Serverless Function - Fashion Photoshoot Backend
Maps FastAPI app to Vercel's serverless environment
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from app.main import app

# Export as ASGI app for Vercel
export = app
