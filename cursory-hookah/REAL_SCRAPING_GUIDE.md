# Real Website Scraping Guide

This guide explains how to use the real website scraping functionality to collect products from major hookah retailers.

## 🎯 Supported Websites

The scraper is configured to work with these major hookah retailers:

- **Hookah-Shisha.com** - Comprehensive hookah retailer
- **5StarHookah.com** - Premium hookah products
- **SouthSmoke.com** - Traditional and modern hookah gear
- **JuicyHookah.com** - Wide selection of hookah products
- **SobeHookah.com** - Hookah accessories and gear

## 🚀 Getting Started

### 1. Reset Database (Required)

First, reset the database to include the new `source_website` field:

```bash
cd backend
python reset_db_with_scraping.py
```

### 2. Start the Backend

```bash
cd backend
python run.py
```

### 3. Start the Frontend

```bash
cd frontend
npm start
```

## 🕷️ Using the Scraper

### Via Web Interface

1. Navigate to the **🕷️ Scraper** tab in the web app
2. Select a website or "All Websites" to scrape
3. Optionally select a specific category (hookah, bowl, hose, hmd)
4. Click "🚀 Start Scraping"
5. Monitor the progress and results

### Via API

You can also trigger scraping via API calls:

```bash
# Scrape all websites
curl -X POST http://localhost:5000/api/scraper/trigger \
  -H "Content-Type: application/json" \
  -d '{"website": "all", "max_pages": 2}'

# Scrape specific website
curl -X POST http://localhost:5000/api/scraper/trigger \
  -H "Content-Type: application/json" \
  -d '{"website": "hookah-shisha", "category": "hookah"}'
```

## 📊 What Gets Scraped

For each product, the scraper collects:

- **Product Name** - Full product title
- **Brand** - Extracted from product name or website
- **Category** - Automatically determined (hookah, bowl, hose, hmd, etc.)
- **Price** - Current retail price
- **Image URL** - Product image
- **Product URL** - Direct link to the product page
- **Rating** - Customer rating (if available)
- **Review Count** - Number of reviews
- **Compatibility Tags** - Generated based on product characteristics
- **Source Website** - Which website the product came from

## 🔧 Scraper Configuration

The scraper is configured in `backend/app/services/real_scrapers.py`:

### Website Configurations

Each website has specific selectors for:
- Product containers
- Product names
- Prices
- Images
- Links
- Ratings

### Rate Limiting

The scraper includes respectful delays:
- 2-4 seconds between page requests
- 5-10 seconds between websites
- User-Agent headers to identify the scraper

### Error Handling

- Graceful handling of missing elements
- Logging of errors and warnings
- Continues scraping even if individual products fail

## 🎯 Product Categories

The scraper supports these categories:

- **hookah** - Complete hookah pipes
- **bowl** - Tobacco bowls and heads
- **hose** - Smoking hoses and tubes
- **hmd** - Heat management devices
- **coal** - Charcoal and heating elements
- **tobacco** - Shisha tobacco and flavors
- **accessory** - Other hookah accessories

## 🔍 Compatibility Tags

Products are automatically tagged with compatibility information:

### Brand-Specific Tags
- `egyptian_hookah` - Khalil Mamoon and traditional brands
- `modern_hookah` - Shika and contemporary brands
- `heat_management` - Kaloud and HMD brands

### Category-Specific Tags
- `wide_base` - Hookahs with wide bases
- `standard_hose` - Traditional hose compatibility
- `washable` - Silicone and washable hoses
- `kaloud_lotus_hmd` - Kaloud Lotus compatibility
- `ceramic` - Ceramic bowls
- `clay` - Traditional clay bowls

## 🛡️ Legal and Ethical Considerations

### Respectful Scraping
- Rate limiting to avoid overwhelming servers
- Proper User-Agent headers
- Respect for robots.txt (implemented in production)

### Data Usage
- Products are stored locally for compatibility analysis
- Direct links to original product pages
- No content is copied or redistributed

### Website Policies
Always check individual website terms of service before scraping.

## 🔧 Troubleshooting

### Common Issues

1. **No products found**
   - Check if the website structure has changed
   - Verify the selectors in the configuration
   - Check network connectivity

2. **Rate limiting**
   - Increase delays between requests
   - Reduce the number of pages scraped
   - Use a VPN if necessary

3. **Database errors**
   - Ensure the database has been reset with the new schema
   - Check that all required fields are present

### Debugging

Enable detailed logging by modifying the scraper:

```python
# In real_scrapers.py
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Monitoring Scraping

### Database Status

Check the scraper status via API:

```bash
curl http://localhost:5000/api/scraper/status
```

### Available Websites

List configured websites:

```bash
curl http://localhost:5000/api/scraper/websites
```

## 🚀 Production Considerations

For production use, consider:

1. **Scheduled Scraping** - Set up cron jobs for regular updates
2. **Incremental Updates** - Only scrape new/changed products
3. **Error Monitoring** - Set up alerts for scraping failures
4. **Data Validation** - Verify scraped data quality
5. **Backup Strategy** - Regular database backups

## 📝 Customization

### Adding New Websites

1. Add website configuration to `self.websites` in `RealHookahScraper`
2. Define CSS selectors for product elements
3. Test with a small number of pages first
4. Add to the websites list in the API

### Modifying Selectors

If a website changes its structure:

1. Inspect the new HTML structure
2. Update the selectors in the configuration
3. Test with a single product first
4. Verify all data is extracted correctly

## 🎉 Success Metrics

Monitor these metrics to ensure successful scraping:

- **Products Found** - Number of products scraped
- **Success Rate** - Percentage of products successfully parsed
- **Data Quality** - Completeness of product information
- **Update Frequency** - How often products are updated

---

**Note**: This scraper is designed for educational and compatibility analysis purposes. Always respect website terms of service and implement appropriate rate limiting for production use. 