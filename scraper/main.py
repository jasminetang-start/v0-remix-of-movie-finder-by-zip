"""
Main Script - Orchestrates all cinema scrapers
"""

import json
import os
import argparse
from datetime import datetime
from typing import List, Dict, Any

from config import main_config, cinemas
from scrapers.siff.scraper import SIFFScraper
from scrapers.siff.processor import SIFFProcessor
# from scrapers.viff.scraper import VIFFScraper
# from scrapers.viff.processor import VIFFProcessor


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    output_path = os.path.join(os.path.dirname(__file__), main_config.OUTPUT_DIR)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")
    return output_path


def save_json(data: Any, filename: str, output_dir: str) -> str:
    """Save data to JSON file"""
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


def run_scraper(scraper_name: str, output_dir: str) -> Dict[str, Any]:
    """
    Run a specific scraper
    
    Args:
        scraper_name: Name of scraper (e.g., "siff", "viff")
        output_dir: Output directory path
        
    Returns:
        Result dictionary with status and data
    """
    result = {
        "scraper": scraper_name,
        "status": "failed",
        "movie_count": 0,
        "error": None,
        "scraped_at": datetime.now().isoformat()
    }
    
    try:
        print(f"\n{'='*60}")
        print(f"▶ RUNNING {scraper_name.upper()} SCRAPER")
        print(f"{'='*60}")
        
        # Get scraper and processor
        if scraper_name == "siff":
            scraper = SIFFScraper()
            processor = SIFFProcessor()
        # elif scraper_name == "viff":
        #     scraper = VIFFScraper()
        #     processor = VIFFProcessor()
        else:
            raise ValueError(f"Unknown scraper: {scraper_name}")
        
        # Get cinema config
        cinema_config = cinemas.get_cinema_config(scraper_name)
        
        # Step 1: Scrape raw data
        print("\n📥 SCRAPING...")
        raw_data = scraper.scrape_all_days()
        
        if not raw_data:
            print(f"⚠️  No data scraped from {scraper_name.upper()}")
            result["status"] = "no_data"
            return result
        
        print(f"✓ Scraped {len(raw_data)} raw entries")
        
        # Step 2: Process data
        print("\n⚙️  PROCESSING...")
        processed_data = processor.process_movies(raw_data)
        
        if not processed_data:
            print(f"⚠️  No data processed from {scraper_name.upper()}")
            result["status"] = "no_data"
            return result
        
        print(f"✓ Processed {len(processed_data)} movies")
        
        # Step 3: Save cinema-specific file
        output_file = cinema_config['output_file']
        filepath = save_json(processed_data, output_file, output_dir)
        print(f"\n💾 Saved to: {filepath}")
        
        # Update result
        result["status"] = "success"
        result["movie_count"] = len(processed_data)
        result["data"] = processed_data
        
        # Cleanup
        scraper.cleanup()
        
        print(f"\n✅ {scraper_name.upper()} scraper completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in {scraper_name.upper()} scraper: {e}")
        import traceback
        traceback.print_exc()
        result["error"] = str(e)
    
    return result


def generate_combined_output(results: List[Dict[str, Any]], output_dir: str):
    """Generate combined movies.json with all cinemas"""
    all_movies = []
    
    for result in results:
        if result["status"] == "success" and "data" in result:
            all_movies.extend(result["data"])
    
    if all_movies:
        filepath = save_json(
            all_movies,
            main_config.COMBINED_OUTPUT_FILE,
            output_dir
        )
        print(f"\n💾 Combined output saved to: {filepath}")
    
    return all_movies


def generate_metadata(results: List[Dict[str, Any]], total_movies: int, output_dir: str):
    """Generate metadata.json with scraping info"""
    metadata = {
        "last_updated": datetime.now().isoformat(),
        "total_movies": total_movies,
        "cinemas": {}
    }
    
    for result in results:
        scraper_name = result["scraper"]
        metadata["cinemas"][scraper_name] = {
            "movie_count": result["movie_count"],
            "last_scraped": result["scraped_at"],
            "status": result["status"]
        }
        if result.get("error"):
            metadata["cinemas"][scraper_name]["error"] = result["error"]
    
    filepath = save_json(metadata, main_config.METADATA_FILE, output_dir)
    print(f"💾 Metadata saved to: {filepath}")
    
    return metadata


def main():
    """Main execution function"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Cinema Showtime Scraper')
    parser.add_argument(
        '--scrapers',
        nargs='+',
        choices=cinemas.get_all_cinema_names(),
        help='Specific scrapers to run (e.g., --scrapers siff viff)'
    )
    args = parser.parse_args()
    
    # Determine which scrapers to run
    scrapers_to_run = args.scrapers if args.scrapers else main_config.ENABLED_SCRAPERS
    
    # Print header
    print("\n" + "="*60)
    print("🎬 CINEMA SHOWTIME SCRAPER")
    print("="*60)
    print(f"Scrapers to run: {', '.join(scrapers_to_run).upper()}")
    print(f"OMDb enrichment: {'ENABLED' if main_config.USE_OMDB_ENRICHMENT else 'DISABLED'}")
    print("="*60)
    
    # Ensure output directory exists
    output_dir = ensure_output_dir()
    
    # Run each scraper
    results = []
    for scraper_name in scrapers_to_run:
        if scraper_name not in cinemas.get_all_cinema_names():
            print(f"\n⚠️  Unknown scraper: {scraper_name}")
            continue
        
        result = run_scraper(scraper_name, output_dir)
        results.append(result)
    
    # Generate combined output
    print(f"\n{'='*60}")
    print("📦 GENERATING COMBINED OUTPUT")
    print(f"{'='*60}")
    
    all_movies = generate_combined_output(results, output_dir)
    
    # Generate metadata
    metadata = generate_metadata(results, len(all_movies), output_dir)
    
    # Print final summary
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total movies across all cinemas: {len(all_movies)}")
    
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} {result['scraper'].upper()}: {result['movie_count']} movies ({result['status']})")
    
    print(f"\n✅ Scraping completed!")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()