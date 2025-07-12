import requests
from bs4 import BeautifulSoup
from app.models.gear import Gear
from app import db
import time
import random
import re
from urllib.parse import urljoin, urlparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealHookahScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Website configurations
        self.websites = {
            'southsmoke': {
                'base_url': 'https://www.southsmoke.com',
                'search_url': 'https://www.southsmoke.com/hookahs',
                'product_selector': '.product-item',
                'name_selector': '.product-name',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'link_selector': '.product-name a',
                'rating_selector': '.rating',
                'category_mapping': {
                    'hookahs': 'hookah',
                    'bowls': 'bowl',
                    'hoses': 'hose',
                    'heat-management': 'hmd'
                }
            },
            '5starhookah': {
                'base_url': 'https://5starhookah.com',
                'search_url': 'https://5starhookah.com/collections/all-hookahs',
                'product_selector': '.product-item, .product, .grid-product, .product-card',
                'name_selector': '.product-title, .grid-product__title, .product-name, .product-card__title, .mt5',
                'price_selector': '.price, .grid-product__price, .product-price, .product-card__price',
                'image_selector': '.product-image img, .grid-product__image img, .product-img img, .product-card__image img',
                'link_selector': '.product-title a, .grid-product__title a, .product-name a, .product-card__title a, a',
                'rating_selector': '.rating, .product-rating',
                'category_mapping': {
                    'hookahs': 'hookah',
                    'bowls': 'bowl',
                    'hoses': 'hose',
                    'heat-management': 'hmd',
                    'shisha': 'tobacco',
                    'charcoal': 'coal',
                    'accessories': 'accessory'
                }
            },
            'sobehookah': {
                'base_url': 'https://www.sobehookah.com',
                'search_url': 'https://www.sobehookah.com/collections/store/Hookah',
                'product_selector': '.product-item',
                'name_selector': '.product-name',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'link_selector': '.product-name a',
                'rating_selector': '.rating',
                'category_mapping': {
                    'hookahs': 'hookah',
                    'bowls': 'bowl',
                    'hoses': 'hose',
                    'heat-management': 'hmd'
                }
            }
        }

    def scrape_website(self, website_name, category=None, max_pages=3):
        """Scrape products from a specific website"""
        if website_name not in self.websites:
            logger.error(f"Unknown website: {website_name}")
            return []
        
        config = self.websites[website_name]
        products = []
        
        # Set current scraping category for context
        self._current_scraping_category = category
        
        try:
            # Determine the URL to scrape
            if category:
                category_url = self._get_category_url(website_name, category)
                if category_url:
                    urls_to_scrape = [category_url]
                    logger.info(f"Using category URL for {website_name}: {category_url}")
                else:
                    urls_to_scrape = [config['search_url']]
                    logger.info(f"No category URL found, using default: {config['search_url']}")
            else:
                urls_to_scrape = [config['search_url']]
                logger.info(f"Using default search URL for {website_name}: {config['search_url']}")
            
            # Scrape multiple pages
            for page in range(1, max_pages + 1):
                for base_url in urls_to_scrape:
                    page_url = f"{base_url}?page={page}" if page > 1 else base_url
                    logger.info(f"Scraping {website_name} - Page {page}: {page_url}")
                    
                    # Validate URL before making request
                    try:
                        from urllib.parse import urlparse
                        parsed_url = urlparse(page_url)
                        logger.info(f"URL validation - Scheme: {parsed_url.scheme}, Netloc: {parsed_url.netloc}, Path: {parsed_url.path}")
                        
                        if not parsed_url.scheme or not parsed_url.netloc:
                            logger.error(f"Invalid URL structure: {page_url}")
                            continue
                            
                    except Exception as e:
                        logger.error(f"URL parsing error for {page_url}: {e}")
                        continue
                    
                    page_products = self._scrape_page(website_name, page_url, config)
                    products.extend(page_products)
                    
                    # Be respectful with delays
                    time.sleep(random.uniform(2, 4))
            
            logger.info(f"Scraped {len(products)} products from {website_name}")
            return products
            
        except Exception as e:
            logger.error(f"Error scraping {website_name}: {e}")
            return []

    def _scrape_page(self, website_name, url, config):
        """Scrape a single page"""
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, timeout=10)
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code} for URL: {url}")
                logger.error(f"Response headers: {dict(response.headers)}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find all product elements
            product_elements = soup.select(config['product_selector'])
            logger.info(f"Found {len(product_elements)} product elements on {website_name}")
            
            for element in product_elements:
                try:
                    product = self._parse_product_element(element, website_name, config)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.warning(f"Error parsing product from {website_name}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(products)} products from {website_name}")
            return products
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")
            return []

    def _parse_product_element(self, element, website_name, config):
        """Parse individual product element"""
        try:
            # Extract product name
            name_elem = element.select_one(config['name_selector'])
            name = name_elem.get_text(strip=True) if name_elem else None
            
            if not name:
                return None
            
            # Extract price
            price_elem = element.select_one(config['price_selector'])
            price_text = price_elem.get_text(strip=True) if price_elem else "$0.00"
            price = self._extract_price(price_text)
            
            # Extract image URL
            img_elem = element.select_one(config['image_selector'])
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(config['base_url'], image_url)
            
            # Extract product URL
            link_elem = element.select_one(config['link_selector'])
            product_url = None
            if link_elem:
                product_url = link_elem.get('href')
                if product_url and not product_url.startswith('http'):
                    product_url = urljoin(config['base_url'], product_url)
            
            # Extract rating
            rating_elem = element.select_one(config['rating_selector'])
            rating = 0.0
            review_count = 0
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Determine category based on URL context, product name, and current scraping category
            current_category = getattr(self, '_current_scraping_category', None)
            category = self._determine_category(name, product_url, config, current_category)
            
            # Extract brand from product name
            brand = self._extract_brand(name, website_name)
            
            # Generate compatibility tags
            compatibility_tags = self._generate_compatibility_tags(name, category, brand)
            
            return {
                'name': name,
                'brand': brand,
                'category': category,
                'price': price,
                'image_url': image_url,
                'product_url': product_url,
                'rating': rating,
                'review_count': review_count,
                'description': f"Product from {website_name}",
                'specifications': {},
                'compatibility_tags': compatibility_tags,
                'source_website': website_name
            }
            
        except Exception as e:
            logger.warning(f"Error parsing product element: {e}")
            return None

    def _extract_price(self, price_text):
        """Extract numeric price from text"""
        price_match = re.search(r'[\$£€]?(\d+\.?\d*)', price_text.replace(',', ''))
        if price_match:
            return float(price_match.group(1))
        return 0.0

    def _extract_brand(self, product_name, website_name):
        """Extract brand from product name"""
        # Enhanced list of hookah brands with variations
        brands = [
            'Khalil Mamoon', 'KM', 'Shika', 'Starbuzz', 'Fumari', 'Tangiers',
            'Al Fakher', 'Nakhla', 'Dokha', 'Kaloud', 'Provost', 'D-Hose',
            'Mya', 'Egyptian', 'Turkish', 'Syrian', 'Modern', 'Traditional',
            'Aeon', 'Alpha', 'Amira', 'Amy Deluxe', 'Amotion', 'Anima',
            'Apocalypse', 'ATH', 'Aura', 'Avion', 'B2', 'BYO', 'Chaos',
            'Cocoyaya', 'Corsair', 'Cube', 'Damla', 'Darkside', 'D-Hookahs',
            'Deezer', 'Don', 'Draco', 'Dschinni', 'DSH', 'DUD', 'El Bomber',
            'El Nefes', 'Electric', 'Elmas', 'Enso', 'Euphoria', 'Everember',
            'Evolution', 'Fantasia', 'Flume', 'Fumant', 'Glass', 'Golden Desert',
            'HJ', 'Honey Sigh', 'Hoob', 'Hookah King', 'Hooky Steel', 'Hume',
            'Japona', 'Jetpack', 'Kalle', 'Koress', 'KVZE', 'Lavoo', 'Luna',
            'Maestro', 'Magdy Zidan', 'Make', 'Mamay Customs', 'Mansory',
            'Mattpear', 'Marajah', 'Mexanika Smoke', 'Midas', 'Misha', 'MG',
            'MIG', 'Mob', 'Modern', 'Moze', 'Na-Grani', 'NAYB', 'Nova Smoke',
            'Nube Unique', 'Nuvo', 'Oduman', 'Omar', 'Overdozz', 'OVO 360',
            'Pandora', 'Portable', 'Regal', 'Retrofit', 'RF', 'Roden',
            'Sahara Smoke', 'Shi Carver', 'Shisha Kings', 'Shishabucks',
            'SHISHATECH', 'Smokah', 'Social Smoke', 'Spaceman', 'Square',
            'Steamulation', 'Supra', 'Tempus', 'Thunder', 'Triton', 'Tyrant',
            'Union', 'Vesper', 'Vogue', 'VZ', 'Wookah', 'Zahrah', 'Zomo',
            'Zord', 'Alpaca', 'OBLAKO', 'LeRook', 'Harmony', 'Musthave',
            'Trifecta', 'Titanium', 'CocoUrth', 'Coco Nara', 'Coco Mazaya',
            'Coco Riki', 'COCOUS', 'Cocourth', 'Coco Primo', 'Coco Ultimate',
            'D\'schinni', 'Exotica', 'Fumax', 'Ghost', 'Green Flame',
            'King of Fire', 'LeOrange', 'Medwakh', 'Native', 'Natural',
            'Nour', 'One Nation', 'Pharaoh\'s', 'Prestige'
        ]
        
        # Try to find exact brand matches first
        for brand in brands:
            if brand.lower() in product_name.lower():
                return brand
        
        # Try to extract brand from common patterns
        name_lower = product_name.lower()
        
        # Look for brand patterns like "Brand Name Product"
        words = product_name.split()
        if len(words) >= 2:
            # Check if first two words might be a brand
            potential_brand = f"{words[0]} {words[1]}"
            if any(brand.lower() in potential_brand.lower() for brand in brands):
                return potential_brand
            
            # Check if first word might be a brand
            if any(brand.lower().startswith(words[0].lower()) for brand in brands):
                for brand in brands:
                    if brand.lower().startswith(words[0].lower()):
                        return brand
        
        # Look for specific brand indicators
        brand_indicators = {
            'aeon': 'Aeon',
            'alpaca': 'Alpaca',
            'oblako': 'OBLAKO',
            'musthave': 'Musthave',
            'trifecta': 'Trifecta',
            'titanium': 'Titanium',
            'cocourth': 'CocoUrth',
            'coco nara': 'Coco Nara',
            'coco mazaya': 'Coco Mazaya',
            'coco riki': 'Coco Riki',
            'cocous': 'COCOUS',
            'coco primo': 'Coco Primo',
            'coco ultimate': 'Coco Ultimate',
            'd\'schinni': 'D\'schinni',
            'exotica': 'Exotica',
            'fumax': 'Fumax',
            'ghost': 'Ghost',
            'green flame': 'Green Flame',
            'king of fire': 'King of Fire',
            'leorange': 'LeOrange',
            'medwakh': 'Medwakh',
            'native': 'Native',
            'natural': 'Natural',
            'nour': 'Nour',
            'one nation': 'One Nation',
            'pharaoh\'s': 'Pharaoh\'s',
            'prestige': 'Prestige'
        }
        
        for indicator, brand in brand_indicators.items():
            if indicator in name_lower:
                return brand
        
        # If no brand found, try to extract from product name structure
        # Many hookah products follow "Brand Name - Product Description" pattern
        if ' - ' in product_name:
            potential_brand = product_name.split(' - ')[0].strip()
            if len(potential_brand.split()) <= 3:  # Likely a brand if 3 words or less
                return potential_brand
        
        # Default brand based on website (only as last resort)
        website_brands = {
            'hookah-shisha': 'Hookah-Shisha',
            '5starhookah': '5StarHookah',
            'southsmoke': 'SouthSmoke',
            'juicyhookah': 'JuicyHookah',
            'sobehookah': 'SobeHookah'
        }
        
        return website_brands.get(website_name, 'Unknown')

    def _determine_category(self, product_name, product_url, config, current_category=None):
        """Determine product category"""
        name_lower = product_name.lower()
        url_lower = product_url.lower() if product_url else ''
        
        # First, use the current scraping category if available
        if current_category:
            return current_category
        
        # Then, try to determine category from URL context
        if 'all-hookahs' in url_lower or 'hookah' in url_lower:
            return 'hookah'
        elif 'all-hookah-bowls' in url_lower or 'bowl' in url_lower:
            return 'bowl'
        elif 'all-shisha' in url_lower or 'shisha' in url_lower:
            return 'tobacco'
        elif 'all-charcoals' in url_lower or 'charcoal' in url_lower:
            return 'coal'
        elif 'all-accessories' in url_lower or 'accessories' in url_lower:
            return 'accessory'
        
        # Fallback to name-based detection
        if any(word in name_lower for word in ['hookah', 'shisha', 'pipe']):
            return 'hookah'
        elif any(word in name_lower for word in ['bowl', 'head']):
            return 'bowl'
        elif any(word in name_lower for word in ['hose', 'tube']):
            return 'hose'
        elif any(word in name_lower for word in ['hmd', 'heat', 'management', 'lotus', 'provost']):
            return 'hmd'
        elif any(word in name_lower for word in ['coal', 'charcoal', 'coco']):
            return 'coal'
        elif any(word in name_lower for word in ['tobacco', 'shisha', 'flavor', 'molasses']):
            return 'tobacco'
        elif any(word in name_lower for word in ['accessory', 'accessories', 'tongs', 'foil', 'grommet']):
            return 'accessory'
        else:
            return 'accessory'

    def _generate_compatibility_tags(self, product_name, category, brand):
        """Generate compatibility tags based on product characteristics"""
        tags = []
        name_lower = product_name.lower()
        
        # Brand-specific tags
        if 'khalil mamoon' in name_lower or 'km' in name_lower:
            tags.extend(['egyptian_hookah', 'traditional', 'brass'])
        elif 'shika' in name_lower:
            tags.extend(['modern_hookah', 'stainless_steel', 'multi_port'])
        elif 'kaloud' in name_lower:
            tags.extend(['heat_management', 'modern', 'temperature_control'])
        
        # Category-specific tags
        if category == 'hookah':
            tags.extend(['wide_base', 'standard_hose'])
        elif category == 'bowl':
            if 'lotus' in name_lower:
                tags.extend(['kaloud_lotus_hmd', 'ceramic', 'heat_management'])
            else:
                tags.extend(['traditional', 'clay', 'foil'])
        elif category == 'hose':
            if 'silicone' in name_lower:
                tags.extend(['washable', 'silicone', 'modern_hookah'])
            else:
                tags.extend(['traditional', 'leather', 'egyptian_hookah'])
        elif category == 'hmd':
            tags.extend(['heat_management', 'stainless_steel'])
        
        return tags

    def _get_category_url(self, website_name, category):
        """Get category-specific URL for a website"""
        category_urls = {
            'southsmoke': {
                'hookah': 'https://www.southsmoke.com/hookahs',
                'bowl': 'https://www.southsmoke.com/bowls',
                'hose': 'https://www.southsmoke.com/hoses',
                'hmd': 'https://www.southsmoke.com/heat-management'
            },
            '5starhookah': {
                'hookah': 'https://5starhookah.com/collections/all-hookahs',
                'bowl': 'https://5starhookah.com/collections/all-hookah-bowls',
                'hose': 'https://5starhookah.com/collections/all-accessories',  # Use accessories as fallback
                'hmd': 'https://5starhookah.com/collections/all-accessories',  # Use accessories as fallback
                'tobacco': 'https://5starhookah.com/collections/all-shisha',
                'coal': 'https://5starhookah.com/collections/all-charcoals',
                'accessory': 'https://5starhookah.com/collections/all-accessories'
            },
            'sobehookah': {
                'hookah': 'https://www.sobehookah.com/collections/store/Hookah',
                'bowl': 'https://www.sobehookah.com/collections/store/Bowl',
                'hose': 'https://www.sobehookah.com/collections/store/Hose',
                'hmd': 'https://www.sobehookah.com/collections/store/Heat-Management'
            }
        }
        
        return category_urls.get(website_name, {}).get(category)

    def scrape_all_websites(self, categories=None, max_pages=2):
        """Scrape all configured websites"""
        all_products = []
        
        for website_name in self.websites.keys():
            logger.info(f"Starting scrape of {website_name}")
            
            if categories:
                for category in categories:
                    products = self.scrape_website(website_name, category, max_pages)
                    all_products.extend(products)
            else:
                products = self.scrape_website(website_name, max_pages=max_pages)
                all_products.extend(products)
            
            # Be respectful with delays between websites
            time.sleep(random.uniform(5, 10))
        
        return all_products

    def save_products_to_db(self, products):
        """Save scraped products to database"""
        added_count = 0
        updated_count = 0
        
        for product_data in products:
            try:
                # Check if product already exists (by name and brand)
                existing = Gear.query.filter_by(
                    name=product_data['name'],
                    brand=product_data['brand']
                ).first()
                
                if existing:
                    # Update existing product
                    existing.price = product_data.get('price', existing.price)
                    existing.image_url = product_data.get('image_url', existing.image_url)
                    existing.product_url = product_data.get('product_url', existing.product_url)
                    existing.rating = product_data.get('rating', existing.rating)
                    existing.review_count = product_data.get('review_count', existing.review_count)
                    updated_count += 1
                else:
                    # Add new product
                    gear = Gear(**product_data)
                    db.session.add(gear)
                    added_count += 1
                    
            except Exception as e:
                logger.error(f"Error saving product {product_data.get('name', 'Unknown')}: {e}")
                continue
        
        try:
            db.session.commit()
            logger.info(f"Database updated: {added_count} new products, {updated_count} updated")
            return {'added': added_count, 'updated': updated_count}
        except Exception as e:
            logger.error(f"Error committing to database: {e}")
            db.session.rollback()
            return {'added': 0, 'updated': 0} 