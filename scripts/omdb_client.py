"""
OMDb API Client - Fetches additional movie information
"""

import requests
import time
from typing import Dict, Any, Optional
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts import config


class OMDbClient:
    """Client for interacting with OMDb API"""
    
    def __init__(self):
        self.api_key = config.OMDB_API_KEY
        self.api_url = config.OMDB_API_URL
        self.cache = {}  # Simple cache to avoid duplicate API calls
    
    def search_by_title_year(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Search for a movie by title and optionally year
        
        Args:
            title: Movie title
            year: Release year (optional but recommended for accuracy)
            
        Returns:
            Movie data from OMDb API or None if not found
        """
        # Check cache first
        cache_key = f"{title}_{year}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            params = {
                'apikey': self.api_key,
                't': title,
                'plot': 'short',  # or 'full' for longer plot
                'r': 'json'
            }
            
            if year:
                params['y'] = year
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if movie was found
            if data.get('Response') == 'True':
                # Cache the result
                self.cache[cache_key] = data
                return data
            else:
                print(f"    OMDb: '{title}' ({year}) not found - {data.get('Error', 'Unknown error')}")
                self.cache[cache_key] = None
                return None
                
        except requests.exceptions.Timeout:
            print(f"    OMDb: Timeout for '{title}'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"    OMDb: Error fetching '{title}': {e}")
            return None
        except Exception as e:
            print(f"    OMDb: Unexpected error for '{title}': {e}")
            return None
    
    def search_by_imdb_id(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        """
        Search for a movie by IMDb ID
        
        Args:
            imdb_id: IMDb ID (e.g., 'tt1285016')
            
        Returns:
            Movie data from OMDb API or None if not found
        """
        # Check cache first
        if imdb_id in self.cache:
            return self.cache[imdb_id]
        
        try:
            params = {
                'apikey': self.api_key,
                'i': imdb_id,
                'plot': 'short',
                'r': 'json'
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') == 'True':
                self.cache[imdb_id] = data
                return data
            else:
                self.cache[imdb_id] = None
                return None
                
        except Exception as e:
            print(f"    OMDb: Error fetching IMDb ID '{imdb_id}': {e}")
            return None
    
    def extract_enrichment_data(self, omdb_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant fields from OMDb response
        
        Args:
            omdb_data: Raw OMDb API response
            
        Returns:
            Dictionary with enriched movie data
        """
        if not omdb_data:
            return {}
        
        def safe_get(key, default=None):
            """Get value from dict, return None if 'N/A' or missing"""
            value = omdb_data.get(key, default)
            return None if value == 'N/A' else value
        
        # Extract ratings
        ratings = {}
        if 'Ratings' in omdb_data:
            for rating in omdb_data['Ratings']:
                source = rating.get('Source', '')
                value = rating.get('Value', '')
                if source == 'Internet Movie Database':
                    ratings['imdb'] = value
                elif source == 'Rotten Tomatoes':
                    ratings['rotten_tomatoes'] = value
                elif source == 'Metacritic':
                    ratings['metacritic'] = value
        
        # Add IMDb rating separately (common use case)
        imdb_rating = safe_get('imdbRating')
        if imdb_rating:
            ratings['imdb_rating'] = imdb_rating
            ratings['imdb_votes'] = safe_get('imdbVotes')
        
        enrichment = {
            'imdb_id': safe_get('imdbID'),
            'plot': safe_get('Plot'),
            'genre': safe_get('Genre'),
            'rated': safe_get('Rated'),  # PG, PG-13, R, etc.
            'actors': safe_get('Actors'),
            'writer': safe_get('Writer'),
            'language': safe_get('Language'),
            'awards': safe_get('Awards'),
            'poster_omdb': safe_get('Poster'),  # OMDb poster URL
            'ratings': ratings if ratings else None,
            'box_office': safe_get('BoxOffice'),
            'production': safe_get('Production')
        }
        
        # Remove None values
        enrichment = {k: v for k, v in enrichment.items() if v is not None}
        
        return enrichment
