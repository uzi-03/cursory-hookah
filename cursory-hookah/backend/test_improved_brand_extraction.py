#!/usr/bin/env python3
"""
Test script to verify improved brand extraction and category detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.real_scrapers import RealHookahScraper
import time

def test_brand_extraction():
    """Test brand extraction with sample product names"""
    print("Testing Brand Extraction")
    print("=" * 50)
    
    scraper = RealHookahScraper()
    
    # Test product names from 5starhookah.com
    test_products = [
        ("Aeon 4th Edition Lounge Hookah", "https://5starhookah.com/products/vyro-evoke"),
        ("Alpaca Rook Bowls", "https://5starhookah.com/products/alpaca-shallow-rook"),
        ("OBLAKO PHUNNEL L Bowl", "https://5starhookah.com/products/copy-of-oblako-phunnel-l-bowl"),
        ("Musthave Hookah Tobacco 125g", "https://5starhookah.com/products/musthave-tobacco"),
        ("Titanium Coconut Charcoal 72pc", "https://5starhookah.com/products/titanium-cube-coconut-charcoal"),
        ("CocoUrth 72pc (Cube)", "https://5starhookah.com/products/cocourth-72pc-cube"),
        ("Hookah Bowl Grommets", "https://5starhookah.com/products/hookah-bowl-grommets"),
        ("HJ Retro Harmony Bowls", "https://5starhookah.com/products/hj-retro-harmony-bowls"),
        ("Al Fakher Tobacco 250g", "https://5starhookah.com/products/al-fakher-250g"),
        ("Trifecta Blonde Leaf Tobacco 250g", "https://5starhookah.com/products/trifecta-250g-1")
    ]
    
    print(f"{'Product Name':<40} {'Brand':<20} {'Category':<15}")
    print("-" * 75)
    
    for product_name, product_url in test_products:
        brand = scraper._extract_brand(product_name, '5starhookah')
        category = scraper._determine_category(product_name, product_url, {})
        
        print(f"{product_name:<40} {brand:<20} {category:<15}")
    
    print("-" * 75)

def test_scraper_with_improved_logic():
    """Test the scraper with improved brand extraction"""
    print("\nTesting Scraper with Improved Logic")
    print("=" * 50)
    
    scraper = RealHookahScraper()
    
    # Test a few categories
    categories_to_test = ['hookah', 'bowl', 'tobacco', 'coal']
    
    for category in categories_to_test:
        print(f"\n--- Testing Category: {category.upper()} ---")
        
        try:
            products = scraper.scrape_website('5starhookah', category=category, max_pages=1)
            
            print(f"Found {len(products)} products")
            
            if products:
                print("Sample products with brands:")
                for i, product in enumerate(products[:5]):  # Show first 5 products
                    print(f"  {i+1}. {product['name']}")
                    print(f"     Brand: {product['brand']}")
                    print(f"     Category: {product['category']}")
                    print()
            
        except Exception as e:
            print(f"Error testing {category}: {e}")
        
        time.sleep(1)  # Be respectful

def test_brand_distribution():
    """Test to see brand distribution in scraped data"""
    print("\nTesting Brand Distribution")
    print("=" * 50)
    
    scraper = RealHookahScraper()
    
    try:
        # Scrape a small sample
        products = scraper.scrape_website('5starhookah', max_pages=1)
        
        # Count brands
        brand_counts = {}
        category_counts = {}
        
        for product in products:
            brand = product['brand']
            category = product['category']
            
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print("Brand Distribution:")
        for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {brand}: {count}")
        
        print("\nCategory Distribution:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Improved Brand Extraction and Category Detection Test")
    print("=" * 60)
    
    # Test brand extraction
    test_brand_extraction()
    
    # Test scraper with improved logic
    test_scraper_with_improved_logic()
    
    # Test brand distribution
    test_brand_distribution()
    
    print("\nTest completed!") 