"""
Movie Scrapers - Fetches raw movie data from SIFF and VIFF websites
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts import config


class BaseScraper:
    """Base scraper class with common functionality"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = None
        
    def setup_selenium(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        if config.USE_HEADLESS:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={config.USER_AGENT}')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def fetch_page(self, url: str) -> str:
        """Fetch page content using Selenium"""
        if not self.driver:
            self.setup_selenium()
        self.driver.get(url)
        time.sleep(config.PAGE_LOAD_WAIT)
        return self.driver.page_source
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html_content, 'html.parser')
    
    def cleanup(self):
        """Close browser and cleanup resources"""
        if self.driver:
            self.driver.quit()


class SIFFScraper(BaseScraper):
    """Scraper for SIFF website"""
    
    def __init__(self):
        super().__init__(config.SIFF_BASE_URL)
        self.cinema_ids = config.SIFF_CINEMA_IDS
    
    def get_cinema_id(self, venue_name: str) -> str:
        """Get cinema ID from venue name"""
        return self.cinema_ids.get(venue_name, f"SIFF_UNKNOWN_{venue_name.upper().replace(' ', '_')}")
    
    def scrape_movies_for_day(self, day_index: int) -> List[Dict[str, Any]]:
        """Scrape movie listings for a specific day"""
        movies = []
        url = f"{self.base_url}?day={day_index}#now"
        
        try:
            print(f"  [SIFF] Fetching day {day_index}...")
            html_content = self.fetch_page(url)
            soup = self.parse_html(html_content)
            
            # Extract the date from button
            button_group = soup.find('div', class_='button-group')
            date_text = 'Unknown'
            if button_group:
                active_button = button_group.find('a', class_='button on')
                if active_button:
                    date_text = active_button.get_text(strip=True)
            
            # Calculate actual date
            actual_date = (datetime.now() + timedelta(days=day_index)).strftime('%Y-%m-%d')
            
            # Find the "Now Playing" section
            listing_section = soup.find('div', class_='listing thumbs')
            
            if not listing_section:
                print(f"    No movies found for day {day_index}")
                return movies
            
            # Find all movie items
            movie_elements = listing_section.find_all('div', class_='item')
            print(f"    Found {len(movie_elements)} movies for {date_text}")
            
            for movie in movie_elements:
                try:
                    # Extract title
                    title_elem = movie.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    if not title:
                        continue
                    
                    # Extract URL
                    title_link = title_elem.find('a') if title_elem else None
                    movie_url = title_link['href'] if title_link and title_link.get('href') else None
                    if movie_url and not movie_url.startswith('http'):
                        movie_url = self.base_url + movie_url
                    
                    # Extract image
                    img_elem = movie.find('img')
                    image_url = img_elem['src'] if img_elem and img_elem.get('src') else None
                    if image_url and not image_url.startswith('http'):
                        image_url = self.base_url + image_url
                    
                    # Extract metadata (country, year, duration, director)
                    meta_elem = movie.find('p', class_='meta')
                    metadata = meta_elem.get_text(strip=True) if meta_elem else ''
                    
                    # Extract venue and showtimes
                    times_section = movie.find('div', class_='times')
                    venue = None
                    showtimes = []
                    
                    if times_section:
                        venue_elem = times_section.find('h3')
                        if venue_elem:
                            venue_link = venue_elem.find('span', class_='dark-gray-text')
                            venue = venue_link.get_text(strip=True) if venue_link else None
                        
                        # Extract all showtime buttons
                        showtime_buttons = times_section.find_all('a', class_='button')
                        for btn in showtime_buttons:
                            time_text = btn.get_text(strip=True)
                            if time_text and ('PM' in time_text or 'AM' in time_text):
                                showtimes.append(time_text)
                    
                    # Create raw movie data entry
                    movie_data = {
                        'title': title,
                        'url': movie_url,
                        'image_url': image_url,
                        'metadata': metadata,
                        'venue': venue,
                        'cinema_id': self.get_cinema_id(venue) if venue else 'SIFF_UNKNOWN',
                        'showtimes': showtimes,
                        'show_date': actual_date,
                        'day_index': day_index,
                        'date_text': date_text
                    }
                    
                    movies.append(movie_data)
                    
                except Exception as e:
                    print(f"    Error parsing movie: {e}")
                    continue
                    
        except Exception as e:
            print(f"    Error scraping day {day_index}: {e}")
        
        return movies
    
    def scrape_all_days(self, days: List[int] = None) -> List[Dict[str, Any]]:
        """Scrape movie listings for multiple days"""
        if days is None:
            days = config.DAYS_TO_SCRAPE
        
        all_movies = []
        
        print(f"\n{'='*60}")
        print(f"SCRAPING SIFF MOVIES")
        print(f"{'='*60}")
        
        for day in days:
            movies = self.scrape_movies_for_day(day)
            all_movies.extend(movies)
            time.sleep(config.REQUEST_DELAY)
        
        print(f"\n{'='*60}")
        print(f"Total SIFF entries scraped: {len(all_movies)}")
        print(f"{'='*60}\n")
        
        return all_movies


class VIFFScraper(BaseScraper):
    """Scraper for VIFF website"""
    
    def __init__(self):
        super().__init__(config.VIFF_BASE_URL)
        self.cinema_ids = config.VIFF_CINEMA_IDS
    
    def get_cinema_id(self, venue_name: str) -> str:
        """Get cinema ID from venue name"""
        return self.cinema_ids.get(venue_name, f"VIFF_UNKNOWN_{venue_name.upper().replace(' ', '_')}")
    
    def scrape_movies_for_day(self, day_index: int) -> List[Dict[str, Any]]:
        """
        Scrape movie listings for a specific day from VIFF
        
        Note: This is a template implementation. The actual HTML structure
        of viff.org needs to be inspected and this method adjusted accordingly.
        """
        movies = []
        
        # VIFF URL structure may be different - adjust as needed
        url = f"{self.base_url}/cinema?day={day_index}"
        
        try:
            print(f"  [VIFF] Fetching day {day_index}...")
            html_content = self.fetch_page(url)
            soup = self.parse_html(html_content)
            
            # Calculate actual date
            actual_date = (datetime.now() + timedelta(days=day_index)).strftime('%Y-%m-%d')
            
            # TODO: Adjust these selectors based on actual VIFF HTML structure
            # This is a template - inspect viff.org to get correct selectors
            
            # Example structure (adjust based on actual site):
            movie_elements = soup.find_all('div', class_='movie-item')  # Adjust selector
            
            if not movie_elements:
                print(f"    No movies found for day {day_index}")
                return movies
            
            print(f"    Found {len(movie_elements)} movies")
            
            for movie in movie_elements:
                try:
                    # Extract title (adjust selector)
                    title_elem = movie.find('h3', class_='movie-title')  # Adjust
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    if not title:
                        continue
                    
                    # Extract URL (adjust selector)
                    title_link = movie.find('a', class_='movie-link')  # Adjust
                    movie_url = title_link['href'] if title_link and title_link.get('href') else None
                    if movie_url and not movie_url.startswith('http'):
                        movie_url = self.base_url + movie_url
                    
                    # Extract image (adjust selector)
                    img_elem = movie.find('img', class_='movie-poster')  # Adjust
                    image_url = img_elem['src'] if img_elem and img_elem.get('src') else None
                    if image_url and not image_url.startswith('http'):
                        image_url = self.base_url + image_url
                    
                    # Extract metadata (adjust selector)
                    meta_elem = movie.find('div', class_='movie-meta')  # Adjust
                    metadata = meta_elem.get_text(strip=True) if meta_elem else ''
                    
                    # Extract venue (adjust selector)
                    venue_elem = movie.find('span', class_='venue-name')  # Adjust
                    venue = venue_elem.get_text(strip=True) if venue_elem else None
                    
                    # Extract showtimes (adjust selector)
                    showtime_elements = movie.find_all('span', class_='showtime')  # Adjust
                    showtimes = [st.get_text(strip=True) for st in showtime_elements]
                    
                    # Create raw movie data entry
                    movie_data = {
                        'title': title,
                        'url': movie_url,
                        'image_url': image_url,
                        'metadata': metadata,
                        'venue': venue,
                        'cinema_id': self.get_cinema_id(venue) if venue else 'VIFF_UNKNOWN',
                        'showtimes': showtimes,
                        'show_date': actual_date,
                        'day_index': day_index,
                        'date_text': actual_date
                    }
                    
                    movies.append(movie_data)
                    
                except Exception as e:
                    print(f"    Error parsing movie: {e}")
                    continue
                    
        except Exception as e:
            print(f"    Error scraping VIFF day {day_index}: {e}")
        
        return movies
    
    def scrape_all_days(self, days: List[int] = None) -> List[Dict[str, Any]]:
        """Scrape movie listings for multiple days"""
        if days is None:
            days = config.DAYS_TO_SCRAPE
        
        all_movies = []
        
        print(f"\n{'='*60}")
        print(f"SCRAPING VIFF MOVIES")
        print(f"{'='*60}")
        
        for day in days:
            movies = self.scrape_movies_for_day(day)
            all_movies.extend(movies)
            time.sleep(config.REQUEST_DELAY)
        
        print(f"\n{'='*60}")
        print(f"Total VIFF entries scraped: {len(all_movies)}")
        print(f"{'='*60}\n")
        
        return all_movies
