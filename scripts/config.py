"""
Configuration file for movie scrapers
"""

# SIFF Configuration
SIFF_BASE_URL = "https://www.siff.net"
SIFF_CINEMA_IDS = {
    "SIFF Cinema Uptown": "SIFF_UPTOWN",
    "SIFF Cinema Downtown": "SIFF_DOWNTOWN",
    "SIFF Film Center": "SIFF_FILM_CENTER",
    "SIFF Cinema Egyptian": "SIFF_EGYPTIAN"
}

# VIFF Configuration
VIFF_BASE_URL = "https://www.viff.org"
VIFF_CINEMA_IDS = {
    "The Centre": "VIFF_CENTRE",
    "International Village": "VIFF_INTERNATIONAL_VILLAGE",
    "Rio Theatre": "VIFF_RIO",
    "Vancity Theatre": "VIFF_VANCITY"
}

# Scraping settings
DAYS_TO_SCRAPE = [0, 1, 2, 3, 4, 5, 6]  # 0 = today, 6 = 6 days from now
REQUEST_DELAY = 1  # seconds between requests (be polite!)
PAGE_LOAD_WAIT = 3  # seconds to wait for JavaScript to load

# Output settings
OUTPUT_DIR = "data"
OUTPUT_FILE = "movies.json"

# Selenium settings
USE_HEADLESS = True  # Run browser in headless mode
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# OMDb API settings
OMDB_API_KEY = "b574d469"  # Your OMDb API key
OMDB_API_URL = "http://www.omdbapi.com/"
USE_OMDB_ENRICHMENT = True  # Set to False to disable OMDb API calls
