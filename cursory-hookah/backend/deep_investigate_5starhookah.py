#!/usr/bin/env python3
"""
Deep investigation of 5starhookah.com HTML structure to find product titles
"""

import requests
from bs4 import BeautifulSoup

def deep_investigate(url):
    """Deep investigation of a single page"""
    print(f"\n=== Deep Investigation of {url} ===")
    
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
            
            # Find product cards
            product_cards = soup.select('.product-card')
            print(f"Found {len(product_cards)} product cards")
            
            if product_cards:
                first_card = product_cards[0]
                print("\n--- Analyzing First Product Card ---")
                
                # Look for any text content that might be a title
                print("All text content in the card:")
                for text in first_card.stripped_strings:
                    print(f"  '{text}'")
                
                # Look for all links
                print("\nAll links in the card:")
                for link in first_card.find_all('a'):
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    print(f"  Link: '{text}' -> {href}")
                
                # Look for all divs with their content
                print("\nAll divs and their content:")
                for div in first_card.find_all('div'):
                    classes = div.get('class', [])
                    text = div.get_text(strip=True)
                    if text:
                        print(f"  Div {classes}: '{text}'")
                
                # Look for h1, h2, h3, h4, h5, h6 tags
                print("\nAll heading tags:")
                for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    headings = first_card.find_all(tag)
                    for heading in headings:
                        text = heading.get_text(strip=True)
                        classes = heading.get('class', [])
                        print(f"  {tag} {classes}: '{text}'")
                
                # Look for spans with potential title content
                print("\nAll spans with text:")
                for span in first_card.find_all('span'):
                    text = span.get_text(strip=True)
                    classes = span.get('class', [])
                    if text:
                        print(f"  Span {classes}: '{text}'")
                
                # Look for any element with 'title' in class name
                print("\nElements with 'title' in class:")
                for elem in first_card.find_all(class_=lambda x: x and 'title' in x):
                    text = elem.get_text(strip=True)
                    classes = elem.get('class', [])
                    print(f"  {elem.name} {classes}: '{text}'")
                
                # Look for any element with 'name' in class name
                print("\nElements with 'name' in class:")
                for elem in first_card.find_all(class_=lambda x: x and 'name' in x):
                    text = elem.get_text(strip=True)
                    classes = elem.get('class', [])
                    print(f"  {elem.name} {classes}: '{text}'")
                
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Test with one URL"""
    url = "https://5starhookah.com/collections/all-hookahs"
    deep_investigate(url)

if __name__ == "__main__":
    main() 