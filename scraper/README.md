# Cinema Aggregator

## 🎬 Project Overview

This monorepo contains:
- **Backend Scraper** (Python) - Scrapes cinema websites for showtimes
- **Data Storage** (JSON) - Versioned showtime data in `data/`
- **Frontend Website** (Coming soon) - Web interface to browse movies
- **GitHub Actions** - Automated daily scraping

```
┌─────────────┐
│  GitHub     │ 
│  Actions    │ ──┐
│  (6AM UTC)  │   │
└─────────────┘   │
                  ▼
            ┌──────────┐        ┌──────────┐
            │  Scraper │───────▶│   data/  │
            │  (Python)│        │   JSON   │
            └──────────┘        └──────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │ Frontend │
                                │ Website  │
                                └──────────┘
```

---

## 🎯 Supported Cinemas

| Cinema | Status | Location |
|--------|--------|----------|
| SIFF | ✅ Working | Seattle, WA |
| VIFF | ⚠️ Placeholder | Vancouver, BC |

---

## 📁 Project Structure

```
cinema-aggregator/
├── .github/
│   └── workflows/
│       └── daily-scrape.yml     # GitHub Action for daily scraping
│
├── scraper/                     # Backend scraper (Python)
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py                  # Entry point
│   │
│   ├── config/                  # Centralized configuration
│   │   ├── main_config.py       # Global settings
│   │   └── cinemas.py           # Cinema-specific configs
│   │
│   ├── common/                  # Shared utilities
│   │   ├── base_scraper.py      # Base scraper class
│   │   ├── base_processor.py    # Base processor class
│   │   └── omdb_client.py       # OMDb API client
│   │
│   └── scrapers/                # Cinema-specific scrapers
│       ├── siff/
│       │   ├── scraper.py
│       │   └── processor.py
│       └── viff/
│           ├── scraper.py
│           └── processor.py
│
├── data/                        # Scraped data (Git-tracked)
│   ├── movies.json              # Combined all cinemas
│   ├── siff_movies.json         # SIFF-specific
│   ├── viff_movies.json         # VIFF-specific
│   └── metadata.json            # Scraping metadata
│
└── website/                     # Frontend (Coming soon)
    └── ...
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Chrome browser
- Git

### Setup Scraper

```bash
# Clone repository
git clone https://github.com/startfilmstudio/cinema-aggregator.git
cd cinema-aggregator

# Navigate to scraper
cd scraper

# Create virtual environment
python3 -m venv siff_env
source siff_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run scraper
python main.py
```

### Run Specific Scrapers

```bash
# Run all enabled scrapers
python main.py

# Run only SIFF
python main.py --scrapers siff

# Run only VIFF
python main.py --scrapers viff

# Run multiple
python main.py --scrapers siff viff
```

---

## ⚙️ Configuration

### Global Settings

Edit `scraper/config/main_config.py`:

```python
# Which scrapers to run
ENABLED_SCRAPERS = ["siff", "viff"]

# OMDb enrichment
OMDB_API_KEY = "your_key_here"
USE_OMDB_ENRICHMENT = True

# Request settings
REQUEST_DELAY = 1  # seconds between requests
USE_HEADLESS = True  # run browser in background
```

### Cinema Settings

Edit `scraper/config/cinemas.py`:

```python
CINEMAS = {
    "siff": {
        "base_url": "https://www.siff.net",
        "days_to_scrape": [0, 1, 2, 3, 4, 5, 6],
        "venues": {
            "SIFF Cinema Uptown": "SIFF_UPTOWN",
            ...
        }
    },
    ...
}
```

---

## 📊 Output Format

### Combined Output (`data/movies.json`)

```json
[
  {
    "movie": {
      "title": "After the Hunt",
      "url": "https://www.siff.net/...",
      "image_url": "https://www.siff.net/images/...",
      "country": "USA",
      "year": 2025,
      "duration": 139,
      "director": "Luca Guadagnino",
      "imdb_id": "tt15239678",
      "imdb_rating": "8.2",
      "plot": "College professor...",
      "genre": "Drama, Thriller",
      "ratings": {
        "imdb": "8.2/10",
        "rotten_tomatoes": "89%"
      }
    },
    "cinema_id": "SIFF_UPTOWN",
    "showtimes": [
      { "show_date": "2025-10-20", "show_time": "19:15" },
      { "show_date": "2025-10-21", "show_time": "19:15" }
    ],
    "scraped_at": "2025-10-20"
  }
]
```

### Metadata (`data/metadata.json`)

```json
{
  "last_updated": "2025-10-20T14:30:00Z",
  "total_movies": 45,
  "cinemas": {
    "siff": {
      "movie_count": 25,
      "last_scraped": "2025-10-20T14:25:00Z",
      "status": "success"
    },
    "viff": {
      "movie_count": 20,
      "status": "success"
    }
  }
}
```

---

## 🤖 GitHub Actions

### Automated Daily Scraping

The scraper runs automatically every day at **6:00 AM UTC** (11 PM PST).

**Workflow:** `.github/workflows/daily-scrape.yml`

```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:      # Manual trigger
```

### Manual Trigger

1. Go to **Actions** tab
2. Select **Daily Movie Scraper**
3. Click **Run workflow**
4. Optional: Specify scrapers (e.g., `siff,viff`)

### Setup GitHub Secrets

For OMDb API enrichment, add your API key:

1. Go to **Settings** → **Secrets** → **Actions**
2. Click **New repository secret**
3. Name: `OMDB_API_KEY`
4. Value: Your OMDb API key
5. Click **Add secret**

---

## 🌐 Frontend Website

### Coming Soon

The frontend will:
- Display movies from `data/movies.json`
- Filter by cinema, date, genre
- Show ratings and showtimes
- Auto-deploy on data updates

### Tech Stack (Planned)

- Framework: Next.js / React
- Deployment: Vercel / Netlify
- Auto-deploy: Triggered by GitHub commits to `data/`

---

## 🛠️ Adding New Cinemas

### Step 1: Add Configuration

Edit `scraper/config/cinemas.py`:

```python
"amc": {
    "name": "AMC Theatres",
    "base_url": "https://www.amctheatres.com",
    "days_to_scrape": [0, 1, 2, 3, 4, 5, 6],
    "output_file": "amc_movies.json",
    "venues": {
        "AMC Pacific Place 11": "AMC_PACIFIC",
        ...
    }
}
```

### Step 2: Create Scraper

Create `scraper/scrapers/amc/scraper.py`:

```python
from common.base_scraper import BaseScraper

class AMCScraper(BaseScraper):
    # Implement AMC-specific scraping logic
    ...
```

### Step 3: Create Processor

Create `scraper/scrapers/amc/processor.py`:

```python
from common.base_processor import BaseProcessor

class AMCProcessor(BaseProcessor):
    # Implement AMC-specific processing logic
    ...
```

### Step 4: Register in Main Script

Edit `scraper/main.py` - add AMC import and conditional.

### Step 5: Enable

Edit `scraper/config/main_config.py`:

```python
ENABLED_SCRAPERS = ["siff", "viff", "amc"]
```

---

## 🐛 Troubleshooting

### Scraper Issues

**Problem:** ChromeDriver error

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

---

**Problem:** No data scraped

**Solution:**
- Website structure may have changed
- Update selectors in `scrapers/{cinema}/scraper.py`
- Set `USE_HEADLESS = False` to see browser

---

**Problem:** OMDb API errors

**Solution:**
- Check API key in config
- Verify daily limit (1,000 requests/day free tier)
- Set `USE_OMDB_ENRICHMENT = False` to disable

---

### GitHub Actions Issues

**Problem:** Action fails to commit

**Solution:**
- Verify GitHub Actions has write permissions
- Go to **Settings** → **Actions** → **General**
- Enable "Read and write permissions"

---

**Problem:** Scraper fails in Actions but works locally

**Solution:**
- Check `OMDB_API_KEY` secret is set
- Verify Chrome installation in workflow
- Check action logs for specific errors

---

## 📝 Development

### Local Development

```bash
# Activate virtual environment
cd scraper
source siff_env/bin/activate

# Run with verbose output
python main.py

# Test specific scraper
python main.py --scrapers siff

# Disable OMDb (faster testing)
# Edit config/main_config.py: USE_OMDB_ENRICHMENT = False
```

### Testing Changes

Before committing:

1. Run scraper locally: `python main.py`
2. Verify output in `../data/`
3. Check `data/metadata.json` for errors
4. Commit changes

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🙏 Acknowledgments

- [OMDb API](http://www.omdbapi.com/) - Movie database
- [Selenium](https://www.selenium.dev/) - Web automation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [GitHub Actions](https://github.com/features/actions) - CI/CD

---

## 📧 Contact

- **GitHub:** [@startfilmstudio](https://github.com/startfilmstudio)
- **Repository:** [cinema-aggregator](https://github.com/startfilmstudio/cinema-aggregator)

---

**Happy scraping! 🎬🍿**