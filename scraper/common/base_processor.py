"""
Base Processor - Shared data processing functionality
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import main_config


class BaseProcessor:
    """Base processor with shared data transformation logic"""
    
    def __init__(self, cinema_venues: Dict[str, str]):
        """
        Initialize processor
        
        Args:
            cinema_venues: Mapping of venue names to cinema IDs
        """
        self.cinema_venues = cinema_venues
    
    def parse_metadata(self, metadata: str) -> Dict[str, Any]:
        """
        Parse metadata string into structured data
        
        Example: "USA | 2025 | 119 min. | Joachim Rønning"
        
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
    
    def convert_time_to_24h(self, time_str: str) -> Optional[str]:
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
    
    def get_cinema_id(self, venue_name: str) -> str:
        """
        Get cinema ID from venue name
        
        Args:
            venue_name: e.g., "SIFF Cinema Uptown"
            
        Returns:
            Cinema ID, e.g., "SIFF_UPTOWN"
        """
        return self.cinema_venues.get(
            venue_name,
            f"UNKNOWN_{venue_name.upper().replace(' ', '_')}"
        )