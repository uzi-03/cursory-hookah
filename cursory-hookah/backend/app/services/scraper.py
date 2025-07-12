import requests
from bs4 import BeautifulSoup
from app.models.gear import Gear
from app import db
import time
import random

class HookahScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_demo(self):
        """Demo scraping function that returns sample data"""
        # This is a mock implementation for the MVP
        # In a real implementation, this would scrape actual websites
        
        demo_products = [
            {
                'name': 'Hookah-Shisha Premium Hookah',
                'category': 'hookah',
                'brand': 'Hookah-Shisha',
                'model': 'Premium',
                'description': 'Premium hookah from Hookah-Shisha.com',
                'price': 129.99,
                'image_url': 'https://via.placeholder.com/400x300/667eea/ffffff?text=Hookah-Shisha+Premium',
                'product_url': 'https://hookah-shisha.com/premium-hookah',
                'specifications': {
                    'height': '30 inches',
                    'material': 'stainless_steel',
                    'base_diameter': '6.5 inches'
                },
                'compatibility_tags': ['modern_hose', 'wide_base', 'premium'],
                'rating': 4.6,
                'review_count': 89
            },
            {
                'name': '5Star Hookah Bowl',
                'category': 'bowl',
                'brand': '5Star',
                'model': 'Premium',
                'description': 'Premium bowl from 5StarHookah.com',
                'price': 24.99,
                'image_url': 'https://via.placeholder.com/400x300/27ae60/ffffff?text=5Star+Bowl',
                'product_url': 'https://5starhookah.com/premium-bowl',
                'specifications': {
                    'material': 'ceramic',
                    'capacity': '20-25g',
                    'diameter': '2.3 inches'
                },
                'compatibility_tags': ['ceramic', 'heat_management', 'modern'],
                'rating': 4.4,
                'review_count': 156
            }
        ]
        
        # Add demo products to database
        added_count = 0
        for product_data in demo_products:
            # Check if product already exists
            existing = Gear.query.filter_by(
                name=product_data['name'],
                brand=product_data['brand']
            ).first()
            
            if not existing:
                gear = Gear(**product_data)
                db.session.add(gear)
                added_count += 1
        
        db.session.commit()
        
        return {
            'scraped_products': len(demo_products),
            'added_to_db': added_count,
            'products': demo_products
        }
    
    def scrape_website(self, website_url):
        """Scrape products from a specific website"""
        try:
            # Add delay to be respectful to the website
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(website_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a placeholder implementation
            # Real implementation would parse the specific website structure
            products = []
            
            # Example parsing logic (would need to be customized per website)
            product_elements = soup.find_all('div', class_='product-item')
            
            for element in product_elements:
                try:
                    product = self._parse_product_element(element, website_url)
                    if product:
                        products.append(product)
                except Exception as e:
                    print(f"Error parsing product: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error scraping {website_url}: {e}")
            return []
    
    def _parse_product_element(self, element, base_url):
        """Parse individual product element from HTML"""
        try:
            # This is a generic parser - would need customization per website
            name_elem = element.find('h2') or element.find('h3') or element.find('a')
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
            
            price_elem = element.find('span', class_='price') or element.find('div', class_='price')
            price_text = price_elem.get_text(strip=True) if price_elem else "$0.00"
            price = self._extract_price(price_text)
            
            # Extract other details based on website structure
            # This is a simplified example
            return {
                'name': name,
                'price': price,
                'category': 'unknown',
                'brand': 'Unknown',
                'description': '',
                'image_url': '',
                'product_url': '',
                'specifications': {},
                'compatibility_tags': [],
                'rating': 0.0,
                'review_count': 0
            }
            
        except Exception as e:
            print(f"Error parsing product element: {e}")
            return None
    
    def _extract_price(self, price_text):
        """Extract numeric price from text"""
        import re
        price_match = re.search(r'[\$£€]?(\d+\.?\d*)', price_text)
        if price_match:
            return float(price_match.group(1))
        return 0.0 