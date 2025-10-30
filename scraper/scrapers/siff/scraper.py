"""
SIFF Scraper - Seattle International Film Festival
"""

import time
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.base_scraper import BaseScraper
from config import main_config, cinemas


class SIFFScraper(BaseScraper):
    """Scraper for SIFF website"""
    
    def __init__(self):
        config = cinemas.get_cinema_config("siff")
        super().__init__(
            cinema_name=config['name'],
            base_url=config['base_url']
        )
        self.config = config
    
    def scrape_movies_for_day(self, day_index: int) -> List[Dict[str, Any]]:
        """
        Scrape movie listings for a specific day
        
        Args:
            day_index: 0-6 (0=today, 1=tomorrow, etc.)
            
        Returns:
            List of raw movie data dictionaries
        """
        movies = []
        url = f"{self.base_url}?day={day_index}#now"
        
        try:
            if main_config.VERBOSE:
                print(f"  Fetching day {day_index}...")
            
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
            actual_date = self.calculate_date(day_index)
            
            # Find the "Now Playing" section
            listing_section = soup.find('div', class_='listing thumbs')
            
            if not listing_section:
                if main_config.VERBOSE:
                    print(f"    No movies found for day {day_index}")
                return movies
            
            # Find all movie items
            movie_elements = listing_section.find_all('div', class_='item')
            if main_config.VERBOSE:
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
                    
                    # Extract metadata
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
                        'showtimes': showtimes,
                        'show_date': actual_date,
                        'day_index': day_index,
                        'date_text': date_text
                    }
                    
                    movies.append(movie_data)
                    
                except Exception as e:
                    if main_config.VERBOSE:
                        print(f"    Error parsing movie: {e}")
                    continue
                    
        except Exception as e:
            print(f"    Error scraping day {day_index}: {e}")
        
        return movies
    
    def scrape_all_days(self, days: List[int] = None) -> List[Dict[str, Any]]:
        """
        Scrape movie listings for multiple days
        
        Args:
            days: List of day indices. If None, uses config
            
        Returns:
            List of all raw movie data
        """
        if days is None:
            days = self.config['days_to_scrape']
        
        all_movies = []
        
        for day in days:
            movies = self.scrape_movies_for_day(day)
            all_movies.extend(movies)
            time.sleep(main_config.REQUEST_DELAY)
        
        return all_movies