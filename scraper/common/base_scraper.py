"""
Base Scraper - Shared scraping functionality for all cinema scrapers
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import main_config


class BaseScraper:
    """Base scraper class with shared functionality"""
    
    def __init__(self, cinema_name: str, base_url: str):
        """
        Initialize base scraper
        
        Args:
            cinema_name: Name of cinema (e.g., "SIFF", "VIFF")
            base_url: Base URL of cinema website
        """
        self.cinema_name = cinema_name
        self.base_url = base_url
        self.driver = None
        
    def setup_selenium(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        if main_config.USE_HEADLESS:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={main_config.USER_AGENT}')
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def fetch_page(self, url: str, wait_time: int = None) -> str:
        """
        Fetch page content using Selenium
        
        Args:
            url: URL to fetch
            wait_time: Optional custom wait time (uses config default if None)
            
        Returns:
            Page HTML content
        """
        if not self.driver:
            self.setup_selenium()
        
        wait = wait_time if wait_time is not None else main_config.PAGE_LOAD_WAIT
        
        self.driver.get(url)
        time.sleep(wait)
        return self.driver.page_source
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content with BeautifulSoup"""
        return BeautifulSoup(html_content, 'html.parser')
    
    def calculate_date(self, day_index: int) -> str:
        """
        Calculate actual date from day index
        
        Args:
            day_index: 0 = today, 1 = tomorrow, etc.
            
        Returns:
            Date string in YYYY-MM-DD format
        """
        return (datetime.now() + timedelta(days=day_index)).strftime('%Y-%m-%d')
    
    def cleanup(self):
        """Close browser and cleanup resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_all_days(self, days: List[int]) -> List[Dict[str, Any]]:
        """
        Scrape movie listings for multiple days
        Must be implemented by child classes
        
        Args:
            days: List of day indices to scrape
            
        Returns:
            List of raw movie data
        """
        raise NotImplementedError("Child class must implement scrape_all_days()")