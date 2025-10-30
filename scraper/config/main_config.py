"""
Main Configuration - Global settings for all scrapers
"""

import os

# ============================================================
# API Keys
# ============================================================
# OMDb API Key (uses environment variable in GitHub Actions)
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'b574d469')  # Fallback for local dev
OMDB_API_URL = "http://www.omdbapi.com/"  # OMDb API endpoint
USE_OMDB_ENRICHMENT = True  # Set to False to disable OMDb enrichment

# ============================================================
# Scraper Settings
# ============================================================
# Which scrapers to run
ENABLED_SCRAPERS = ["siff", "viff"]  # Options: "siff", "viff"

# Request settings
REQUEST_DELAY = 1  # Seconds between requests (be polite!)
PAGE_LOAD_WAIT = 3  # Seconds to wait for JavaScript to load

# Selenium settings
USE_HEADLESS = True  # Run browser in headless mode
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ============================================================
# Output Settings
# ============================================================
# Output directory (relative to scraper/ folder)
OUTPUT_DIR = "../data"

# Output filenames
COMBINED_OUTPUT_FILE = "movies.json"  # All cinemas combined
METADATA_FILE = "metadata.json"  # Scraping metadata

# ============================================================
# Logging
# ============================================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
VERBOSE = True  # Print detailed progress messages