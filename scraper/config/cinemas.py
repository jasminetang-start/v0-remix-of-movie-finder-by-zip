"""
Cinema-Specific Configuration
Define base URLs, venue mappings, and scraping parameters for each cinema
"""

CINEMAS = {
    "siff": {
        "name": "Seattle International Film Festival",
        "base_url": "https://www.siff.net",
        "days_to_scrape": [0, 1, 2, 3, 4, 5, 6],  # 0 = today, 6 = 6 days from now
        "output_file": "siff_movies.json",
        "venues": {
            "SIFF Cinema Uptown": "SIFF_UPTOWN",
            "SIFF Cinema Downtown": "SIFF_DOWNTOWN",
            "SIFF Film Center": "SIFF_FILM_CENTER",
            "SIFF Cinema Egyptian": "SIFF_EGYPTIAN"
        }
    },
    
    "viff": {
        "name": "Vancouver International Film Festival",
        "base_url": "https://www.viff.org",
        "days_to_scrape": [0, 1, 2, 3, 4, 5, 6],
        "output_file": "viff_movies.json",
        "venues": {
            "The Centre": "VIFF_CENTRE",
            "International Village": "VIFF_INTERNATIONAL_VILLAGE",
            "Rio Theatre": "VIFF_RIO",
            "Vancity Theatre": "VIFF_VANCITY"
        }
    }
}


def get_cinema_config(cinema_name: str) -> dict:
    """
    Get configuration for a specific cinema
    
    Args:
        cinema_name: Name of the cinema (e.g., "siff", "viff")
        
    Returns:
        Cinema configuration dictionary
    """
    if cinema_name not in CINEMAS:
        raise ValueError(f"Unknown cinema: {cinema_name}. Available: {list(CINEMAS.keys())}")
    
    return CINEMAS[cinema_name]


def get_all_cinema_names() -> list:
    """Get list of all available cinema names"""
    return list(CINEMAS.keys())