#!/usr/bin/env python3
"""
Main entry point for running the movie scraper.
Run this file directly: python scripts/run_scraper.py
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now import from scripts package
from scripts.main import main

if __name__ == "__main__":
    main()
