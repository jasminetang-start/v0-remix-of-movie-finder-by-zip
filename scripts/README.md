# Movie Scraper Scripts

This directory contains Python scripts to scrape movie showtimes from SIFF (Seattle International Film Festival) and VIFF (Vancouver International Film Festival) websites.

## Files

- `main.py` - Main orchestrator script
- `scraper.py` - Web scraping logic for SIFF and VIFF
- `processor.py` - Data processing and transformation
- `omdb_client.py` - OMDb API integration for movie enrichment
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies

## Setup

### Local Development

1. Install Python dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Install Chrome/Chromium browser (required for Selenium)

3. Run the scraper:
\`\`\`bash
cd scripts
python main.py
\`\`\`

The script will:
- Scrape movie data from SIFF and VIFF websites
- Enrich data with OMDb API (ratings, plot, cast, etc.)
- Save results to `data/movies.json`

## Configuration

Edit `config.py` to customize:
- `DAYS_TO_SCRAPE` - Which days to scrape (0=today, 1=tomorrow, etc.)
- `USE_OMDB_ENRICHMENT` - Enable/disable OMDb API enrichment
- `OMDB_API_KEY` - Your OMDb API key
- Cinema ID mappings for SIFF and VIFF venues

## GitHub Actions

The scraper runs automatically via GitHub Actions:
- **Schedule**: Daily at 2 AM UTC (configurable in `.github/workflows/scrape-movies.yml`)
- **Manual trigger**: Can be triggered manually from GitHub Actions tab
- **Auto-commit**: Automatically commits updated `movies.json` to the repository

## VIFF Scraper Note

The VIFF scraper (`VIFFScraper` class in `scraper.py`) is a template implementation. You need to:

1. Visit https://www.viff.org and inspect their cinema/showtimes page
2. Update the CSS selectors in `VIFFScraper.scrape_movies_for_day()` to match their HTML structure
3. Adjust the URL pattern if needed

The SIFF scraper is fully functional and can be used as a reference.

## OMDb API

The scraper uses the OMDb API to enrich movie data with:
- IMDb ratings and votes
- Rotten Tomatoes scores
- Metacritic scores
- Plot summaries
- Cast and crew information
- Genre, rating (PG, R, etc.)
- Awards and box office data

Get a free API key at: http://www.omdbapi.com/apikey.aspx
