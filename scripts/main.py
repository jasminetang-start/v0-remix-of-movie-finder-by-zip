"""
Main script to orchestrate movie scraping from SIFF and VIFF
"""

import json
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts.scraper import SIFFScraper, VIFFScraper
from scripts.processor import MovieProcessor
from scripts import config


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        print(f"Created output directory: {config.OUTPUT_DIR}")


def save_json(data, filename):
    """Save data to JSON file"""
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Data saved to: {filepath}")
    return filepath


def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("MOVIE SCRAPER - SIFF & VIFF")
    print("="*60)
    print(f"SIFF Base URL: {config.SIFF_BASE_URL}")
    print(f"VIFF Base URL: {config.VIFF_BASE_URL}")
    print(f"Days to scrape: {config.DAYS_TO_SCRAPE}")
    print(f"Output file: {config.OUTPUT_FILE}")
    print("="*60 + "\n")
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Initialize scrapers and processor
    siff_scraper = SIFFScraper()
    viff_scraper = VIFFScraper()
    processor = MovieProcessor()
    
    all_raw_data = []
    
    try:
        # Step 1: Scrape SIFF
        print("\n🎬 Starting SIFF scraping...")
        siff_data = siff_scraper.scrape_all_days()
        all_raw_data.extend(siff_data)
        siff_scraper.cleanup()
        
        # Step 2: Scrape VIFF
        print("\n🎬 Starting VIFF scraping...")
        viff_data = viff_scraper.scrape_all_days()
        all_raw_data.extend(viff_data)
        viff_scraper.cleanup()
        
        if not all_raw_data:
            print("❌ No data scraped from any source. Exiting.")
            return
        
        print(f"\n📊 Total raw entries from all sources: {len(all_raw_data)}")
        
        # Step 3: Process combined data
        processed_data = processor.process_movies(all_raw_data)
        
        if not processed_data:
            print("❌ No data processed. Exiting.")
            return
        
        # Step 4: Save processed data
        output_path = save_json(processed_data, config.OUTPUT_FILE)
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"SIFF movies: {len(siff_data)}")
        print(f"VIFF movies: {len(viff_data)}")
        print(f"Total processed movies: {len(processed_data)}")
        print(f"Output saved to: {output_path}")
        
        # Print sample
        if processed_data:
            print("\nSample movie:")
            print(json.dumps(processed_data[0], indent=2))
        
        print("\n✅ Scraping completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        siff_scraper.cleanup()
        viff_scraper.cleanup()
        print("\n🧹 Cleaned up resources")


if __name__ == "__main__":
    main()
