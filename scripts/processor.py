"""
Data Processor - Transforms raw scraped data into desired format
"""

import re
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict
import time
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts import config
from scripts.omdb_client import OMDbClient


class MovieProcessor:
    """Process raw movie data into structured format"""
    
    def __init__(self, use_omdb: bool = None):
        self.use_omdb = use_omdb if use_omdb is not None else config.USE_OMDB_ENRICHMENT
        self.omdb_client = OMDbClient() if self.use_omdb else None
    
    def parse_metadata(self, metadata: str) -> Dict[str, Any]:
        """
        Parse metadata string into structured data
        
        Example input: "USA | 2025 | 119 min. | Joachim Rønning"
        
        Returns:
            {
                "country": "USA",
                "year": 2025,
                "duration": 119,
                "director": "Joachim Rønning"
            }
        """
        result = {
            "country": None,
            "year": None,
            "duration": None,
            "director": None
        }
        
        if not metadata:
            return result
        
        # Split by pipe
        parts = [p.strip() for p in metadata.split('|')]
        
        if len(parts) >= 1:
            result['country'] = parts[0]
        
        if len(parts) >= 2:
            # Try to extract year
            year_match = re.search(r'\b(19|20)\d{2}\b', parts[1])
            if year_match:
                result['year'] = int(year_match.group())
        
        if len(parts) >= 3:
            # Try to extract duration (minutes)
            duration_match = re.search(r'(\d+)\s*min', parts[2])
            if duration_match:
                result['duration'] = int(duration_match.group(1))
        
        if len(parts) >= 4:
            result['director'] = parts[3]
        
        return result
    
    def convert_time_to_24h(self, time_str: str) -> str:
        """
        Convert time string to 24-hour format
        
        Examples:
            "7:00 PM" -> "19:00"
            "10:30 AM" -> "10:30"
        """
        try:
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            return time_obj.strftime('%H:%M')
        except:
            return None
    
    def group_by_movie_and_venue(self, raw_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group raw data by (title, venue) combination
        
        Returns:
            Dictionary with key = (title, venue), value = list of entries
        """
        grouped = defaultdict(list)
        
        for entry in raw_data:
            key = (entry['title'], entry['venue'])
            grouped[key].append(entry)
        
        return grouped
    
    def process_movies(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform raw scraped data into desired format
        
        Args:
            raw_data: List of raw movie entries from scraper
            
        Returns:
            List of processed movie objects in final format
        """
        print(f"\n{'='*60}")
        print(f"PROCESSING DATA")
        print(f"{'='*60}")
        
        # Group by (title, venue)
        grouped = self.group_by_movie_and_venue(raw_data)
        
        print(f"  Grouped into {len(grouped)} unique movie-venue combinations")
        
        if self.use_omdb:
            print(f"  OMDb enrichment: ENABLED")
        else:
            print(f"  OMDb enrichment: DISABLED")
        
        processed_movies = []
        scraped_at = datetime.now().strftime('%Y-%m-%d')
        
        for idx, ((title, venue), entries) in enumerate(grouped.items(), 1):
            # Use first entry as reference for movie details
            first_entry = entries[0]
            
            # Parse metadata
            parsed_meta = self.parse_metadata(first_entry['metadata'])
            
            # Get cinema ID from entry
            cinema_id = first_entry.get('cinema_id', 'UNKNOWN')
            
            # Collect all showtimes across all days
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
            
            # Sort showtimes by date and time
            showtimes.sort(key=lambda x: (x['show_date'], x['show_time']))
            
            # Build base movie object
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
            
            # Enrich with OMDb data if enabled
            if self.use_omdb:
                print(f"  [{idx}/{len(grouped)}] Processing: {title} @ {cinema_id}")
                omdb_data = self.omdb_client.search_by_title_year(
                    title=title,
                    year=parsed_meta['year']
                )
                
                if omdb_data:
                    enrichment = self.omdb_client.extract_enrichment_data(omdb_data)
                    # Merge enrichment data into movie object
                    movie_obj['movie'].update(enrichment)
                    print(f"    ✓ Enriched with OMDb data (IMDb: {enrichment.get('imdb_rating', 'N/A')})")
                else:
                    print(f"    ⚠ No OMDb data found")
                
                # Be polite - small delay between API calls
                time.sleep(0.3)
            else:
                print(f"  ✓ Processed: {title} @ {cinema_id} ({len(showtimes)} showtimes)")
            
            processed_movies.append(movie_obj)
        
        print(f"\n{'='*60}")
        print(f"Total processed movies: {len(processed_movies)}")
        print(f"{'='*60}\n")
        
        return processed_movies
