#!/usr/bin/env python3
"""
Investigate the HTML structure of 5starhookah.com to get correct selectors
"""

import requests
from bs4 import BeautifulSoup
import json

def investigate_page(url, description):
    """Investigate the HTML structure of a page"""
    print(f"\n=== Investigating {description} ===")
    print(f"URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for product cards
            product_cards = soup.select('.product-card')
            print(f"Found {len(product_cards)} product cards")
            
            if product_cards:
                # Analyze the first product card
                first_card = product_cards[0]
                print("\n--- First Product Card Structure ---")
                
                # Find title
                title_selectors = [
                    '.product-card__title',
                    '.product-title',
                    'h3',
                    'h4',
                    '.title'
                ]
                
                title = None
                title_selector = None
                for selector in title_selectors:
                    title_elem = first_card.select_one(selector)
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        title_selector = selector
                        break
                
                print(f"Title: {title}")
                print(f"Title Selector: {title_selector}")
                
                # Find price
                price_selectors = [
                    '.product-card__price',
                    '.price',
                    '.product-price',
                    '[data-price]'
                ]
                
                price = None
                price_selector = None
                for selector in price_selectors:
                    price_elem = first_card.select_one(selector)
                    if price_elem:
                        price = price_elem.get_text(strip=True)
                        price_selector = selector
                        break
                
                print(f"Price: {price}")
                print(f"Price Selector: {price_selector}")
                
                # Find image
                img_selectors = [
                    '.product-card__image img',
                    '.product-image img',
                    'img'
                ]
                
                image_url = None
                image_selector = None
                for selector in img_selectors:
                    img_elem = first_card.select_one(selector)
                    if img_elem:
                        image_url = img_elem.get('src') or img_elem.get('data-src')
                        image_selector = selector
                        break
                
                print(f"Image URL: {image_url}")
                print(f"Image Selector: {image_selector}")
                
                # Find link
                link_selectors = [
                    '.product-card__title a',
                    '.product-title a',
                    'a'
                ]
                
                link_url = None
                link_selector = None
                for selector in link_selectors:
                    link_elem = first_card.select_one(selector)
                    if link_elem:
                        link_url = link_elem.get('href')
                        link_selector = selector
                        break
                
                print(f"Link URL: {link_url}")
                print(f"Link Selector: {link_selector}")
                
                # Show all classes on the first card
                print("\n--- All Classes on First Card ---")
                all_classes = first_card.get('class', [])
                print(f"Classes: {all_classes}")
                
                # Show child elements
                print("\n--- Child Elements ---")
                for child in first_card.children:
                    if hasattr(child, 'name') and child.name:
                        print(f"  {child.name}: {child.get('class', [])}")
                
                return {
                    'title_selector': title_selector,
                    'price_selector': price_selector,
                    'image_selector': image_selector,
                    'link_selector': link_selector,
                    'product_selector': '.product-card'
                }
            
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Investigate multiple pages"""
    urls_to_test = [
        ('https://5starhookah.com/collections/all-hookahs', 'All Hookahs'),
        ('https://5starhookah.com/collections/all-shisha', 'All Shisha'),
        ('https://5starhookah.com/collections/all-charcoals', 'All Charcoals')
    ]
    
    results = {}
    
    for url, description in urls_to_test:
        result = investigate_page(url, description)
        if result:
            results[description] = result
    
    print("\n" + "=" * 50)
    print("SUMMARY OF SELECTORS:")
    print("=" * 50)
    
    for description, selectors in results.items():
        print(f"\n{description}:")
        for key, value in selectors.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 