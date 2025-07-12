#!/usr/bin/env python3
"""
Test the updated working URLs for hookah websites
"""

import requests

def test_url(url, name):
    """Test if a URL is accessible"""
    print(f"\nTesting {name}: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS - URL is accessible")
            print(f"  Content Length: {len(response.content)} bytes")
            return True
        else:
            print(f"  ❌ FAILED - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ ERROR - {e}")
        return False

def main():
    """Test all updated website URLs"""
    websites = {
        'southsmoke': {
            'base_url': 'https://www.southsmoke.com',
            'search_url': 'https://www.southsmoke.com/hookahs',
            'hookah_url': 'https://www.southsmoke.com/hookahs',
            'bowl_url': 'https://www.southsmoke.com/bowls',
            'hose_url': 'https://www.southsmoke.com/hoses',
            'hmd_url': 'https://www.southsmoke.com/heat-management'
        },
        '5starhookah': {
            'base_url': 'https://5starhookah.com',
            'search_url': 'https://5starhookah.com/collections/all-hookahs',
            'hookah_url': 'https://5starhookah.com/collections/all-hookahs',
            'bowl_url': 'https://5starhookah.com/collections/bowls',
            'hose_url': 'https://5starhookah.com/collections/hoses',
            'hmd_url': 'https://5starhookah.com/collections/heat-management'
        },
        'sobehookah': {
            'base_url': 'https://www.sobehookah.com',
            'search_url': 'https://www.sobehookah.com/collections/store/Hookah',
            'hookah_url': 'https://www.sobehookah.com/collections/store/Hookah',
            'bowl_url': 'https://www.sobehookah.com/collections/store/Bowl',
            'hose_url': 'https://www.sobehookah.com/collections/store/Hose',
            'hmd_url': 'https://www.sobehookah.com/collections/store/Heat-Management'
        }
    }
    
    print("🔍 Testing Updated Website URLs")
    print("=" * 50)
    
    working_count = 0
    total_count = 0
    
    for website_name, urls in websites.items():
        print(f"\n📋 {website_name.upper()}")
        print("-" * 30)
        
        # Test base URL
        if test_url(urls['base_url'], f"{website_name} base"):
            working_count += 1
        total_count += 1
        
        # Test search URL
        if test_url(urls['search_url'], f"{website_name} search"):
            working_count += 1
        total_count += 1
        
        # Test category URLs
        for category in ['hookah', 'bowl', 'hose', 'hmd']:
            url_key = f'{category}_url'
            if url_key in urls:
                if test_url(urls[url_key], f"{website_name} {category}"):
                    working_count += 1
                total_count += 1
    
    print(f"\n📊 Summary:")
    print(f"Working URLs: {working_count}/{total_count}")
    print(f"Success Rate: {(working_count/total_count)*100:.1f}%")

if __name__ == '__main__':
    main() 