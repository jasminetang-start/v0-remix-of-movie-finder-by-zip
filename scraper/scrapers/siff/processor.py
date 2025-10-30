"""
SIFF Processor - Process SIFF scraped data
"""

from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.base_processor import BaseProcessor
from common.omdb_client import OMDbClient
from config import main_config, cinemas


class SIFFProcessor(BaseProcessor):
    """Process SIFF movie data"""
    
    def __init__(self, use_omdb: bool = None):
        config = cinemas.get_cinema_config("siff")
        super().__init__(cinema_venues=config['venues'])
        self.use_omdb = use_omdb if use_omdb is not None else main_config.USE_OMDB_ENRICHMENT
        self.omdb_client = OMDbClient() if self.use_omdb else None
    
    def group_by_movie_and_venue(self, raw_data: List[Dict[str, Any]]) -> Dict[tuple, List[Dict[str, Any]]]:
        """Group raw data by (title, venue) combination"""
        grouped = defaultdict(list)
        
        for entry in raw_data:
            key = (entry['title'], entry['venue'])
            grouped[key].append(entry)
        
        return grouped
    
    def process_movies(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform raw scraped data into final format
        
        Args:
            raw_data: List of raw movie entries from scraper
            
        Returns:
            List of processed movie objects
        """
        # Group by (title, venue)
        grouped = self.group_by_movie_and_venue(raw_data)
        
        if main_config.VERBOSE:
            print(f"  Grouped into {len(grouped)} unique movie-venue combinations")
            if self.use_omdb:
                print(f"  OMDb enrichment: ENABLED")
        
        processed_movies = []
        scraped_at = datetime.now().strftime('%Y-%m-%d')
        
        for idx, ((title, venue), entries) in enumerate(grouped.items(), 1):
            first_entry = entries[0]
            
            # Parse metadata
            parsed_meta = self.parse_metadata(first_entry['metadata'])
            
            # Get cinema ID
            cinema_id = self.get_cinema_id(venue) if venue else "SIFF_UNKNOWN"
            
            # Collect all showtimes
            showtimes = []
            for entry in entries:
                show_date = entry['show_date']
                for time_str in entry['showtimes']:
                    time_24h = self.convert_time_to_24h(time_str)
                    if time_24h:
                        showtimes.append({
                            "show_date": show_date,
                            "show_time": time_24h
                        })
            
            # Sort showtimes
            showtimes.sort(key=lambda x: (x['show_date'], x['show_time']))
            
            # Build movie object
            movie_obj = {
                "movie": {
                    "title": title,
                    "url": first_entry['url'],
                    "image_url": first_entry['image_url'],
                    "country": parsed_meta['country'],
                    "year": parsed_meta['year'],
                    "duration": parsed_meta['duration'],
                    "director": parsed_meta['director']
                },
                "cinema_id": cinema_id,
                "showtimes": showtimes,
                "scraped_at": scraped_at
            }
            
            # Enrich with OMDb
            if self.use_omdb:
                if main_config.VERBOSE:
                    print(f"  [{idx}/{len(grouped)}] Processing: {title} @ {cinema_id}")
                
                omdb_data = self.omdb_client.search_by_title_year(
                    title=title,
                    year=parsed_meta['year']
                )
                
                if omdb_data:
                    enrichment = self.omdb_client.extract_enrichment_data(omdb_data)
                    movie_obj['movie'].update(enrichment)
                    if main_config.VERBOSE:
                        print(f"    ✓ Enriched (IMDb: {enrichment.get('imdb_rating', 'N/A')})")
                else:
                    if main_config.VERBOSE:
                        print(f"    ⚠ No OMDb data")
                
                time.sleep(0.3)
            else:
                if main_config.VERBOSE:
                    print(f"  ✓ Processed: {title} @ {cinema_id} ({len(showtimes)} showtimes)")
            
            processed_movies.append(movie_obj)
        
        return processed_movies