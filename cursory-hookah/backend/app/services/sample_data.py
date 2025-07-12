from app import db
from app.models.gear import Gear

def initialize_sample_data():
    """Initialize the database with sample hookah gear data"""
    
    sample_gear = [
        # Hookahs
        {
            'name': 'Khalil Mamoon Classic',
            'category': 'hookah',
            'brand': 'Khalil Mamoon',
            'model': 'Classic',
            'description': 'Traditional Egyptian hookah with brass construction',
            'price': 89.99,
            'image_url': 'https://example.com/km-classic.jpg',
            'product_url': 'https://example.com/km-classic',
            'specifications': {
                'height': '28 inches',
                'material': 'brass',
                'base_diameter': '6 inches',
                'hose_ports': 1
            },
            'compatibility_tags': ['standard_hose', 'egyptian_bowl', 'wide_base'],
            'rating': 4.5,
            'review_count': 127
        },
        {
            'name': 'Shika Hookah',
            'category': 'hookah',
            'brand': 'Shika',
            'model': 'V4',
            'description': 'Modern hookah with advanced features',
            'price': 149.99,
            'image_url': 'https://example.com/shika-v4.jpg',
            'product_url': 'https://example.com/shika-v4',
            'specifications': {
                'height': '32 inches',
                'material': 'stainless_steel',
                'base_diameter': '7 inches',
                'hose_ports': 2
            },
            'compatibility_tags': ['modern_hose', 'phunnel_bowl', 'wide_base', 'multi_port'],
            'rating': 4.7,
            'review_count': 89
        },
        
        # Bowls
        {
            'name': 'Kaloud Lotus Bowl',
            'category': 'bowl',
            'brand': 'Kaloud',
            'model': 'Lotus',
            'description': 'Premium ceramic bowl designed for heat management',
            'price': 34.99,
            'image_url': 'https://example.com/kaloud-lotus.jpg',
            'product_url': 'https://example.com/kaloud-lotus',
            'specifications': {
                'material': 'ceramic',
                'capacity': '25-30g',
                'diameter': '2.5 inches',
                'depth': '1.2 inches'
            },
            'compatibility_tags': ['kaloud_lotus_hmd', 'ceramic', 'heat_management'],
            'rating': 4.8,
            'review_count': 234
        },
        {
            'name': 'Egyptian Clay Bowl',
            'category': 'bowl',
            'brand': 'Traditional',
            'model': 'Egyptian',
            'description': 'Classic Egyptian clay bowl for traditional smoking',
            'price': 12.99,
            'image_url': 'https://example.com/egyptian-bowl.jpg',
            'product_url': 'https://example.com/egyptian-bowl',
            'specifications': {
                'material': 'clay',
                'capacity': '15-20g',
                'diameter': '2 inches',
                'depth': '0.8 inches'
            },
            'compatibility_tags': ['traditional', 'clay', 'foil'],
            'rating': 4.2,
            'review_count': 156
        },
        
        # Heat Management Devices
        {
            'name': 'Kaloud Lotus 1+',
            'category': 'hmd',
            'brand': 'Kaloud',
            'model': 'Lotus 1+',
            'description': 'Advanced heat management device with temperature control',
            'price': 89.99,
            'image_url': 'https://example.com/kaloud-lotus-hmd.jpg',
            'product_url': 'https://example.com/kaloud-lotus-hmd',
            'specifications': {
                'material': 'stainless_steel',
                'diameter': '2.5 inches',
                'weight': '180g',
                'coals': '3-4 pieces'
            },
            'compatibility_tags': ['kaloud_lotus_bowl', 'stainless_steel', 'temperature_control'],
            'rating': 4.9,
            'review_count': 445
        },
        {
            'name': 'Provost Heat Management',
            'category': 'hmd',
            'brand': 'Provost',
            'model': 'Standard',
            'description': 'Foil-based heat management device',
            'price': 24.99,
            'image_url': 'https://example.com/provost-hmd.jpg',
            'product_url': 'https://example.com/provost-hmd',
            'specifications': {
                'material': 'stainless_steel',
                'diameter': '2.2 inches',
                'weight': '120g',
                'coals': '2-3 pieces'
            },
            'compatibility_tags': ['foil_compatible', 'traditional_bowl', 'stainless_steel'],
            'rating': 4.6,
            'review_count': 178
        },
        
        # Hoses
        {
            'name': 'D-Hose Aluminum',
            'category': 'hose',
            'brand': 'D-Hose',
            'model': 'Aluminum',
            'description': 'Washable silicone hose with aluminum handle',
            'price': 39.99,
            'image_url': 'https://example.com/dhose-aluminum.jpg',
            'product_url': 'https://example.com/dhose-aluminum',
            'specifications': {
                'material': 'silicone',
                'length': '72 inches',
                'handle': 'aluminum',
                'washable': True
            },
            'compatibility_tags': ['washable', 'silicone', 'modern_hookah'],
            'rating': 4.7,
            'review_count': 203
        },
        {
            'name': 'Traditional Leather Hose',
            'category': 'hose',
            'brand': 'Traditional',
            'model': 'Leather',
            'description': 'Classic leather hose for traditional smoking',
            'price': 19.99,
            'image_url': 'https://example.com/leather-hose.jpg',
            'product_url': 'https://example.com/leather-hose',
            'specifications': {
                'material': 'leather',
                'length': '60 inches',
                'handle': 'wooden',
                'washable': False
            },
            'compatibility_tags': ['traditional', 'leather', 'egyptian_hookah'],
            'rating': 4.1,
            'review_count': 92
        }
    ]
    
    for gear_data in sample_gear:
        gear = Gear(**gear_data)
        db.session.add(gear)
    
    db.session.commit()
    print(f"Initialized database with {len(sample_gear)} sample gear items") 