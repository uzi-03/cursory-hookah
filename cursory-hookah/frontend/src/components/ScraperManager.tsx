import React, { useState, useEffect } from 'react';
import { scraperApi } from '../services/api';
import { Website, ScrapingStatus } from '../types';

const ScraperManager: React.FC = () => {
  const [websites, setWebsites] = useState<Website[]>([]);
  const [status, setStatus] = useState<ScrapingStatus | null>(null);
  const [selectedWebsite, setSelectedWebsite] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [isScraping, setIsScraping] = useState(false);
  const [scrapingResult, setScrapingResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadWebsites();
    loadStatus();
  }, []);

  const loadWebsites = async () => {
    try {
      const response = await scraperApi.getWebsites();
      if (response.success) {
        setWebsites(response.data);
      }
    } catch (error) {
      console.error('Error loading websites:', error);
    }
  };

  const loadStatus = async () => {
    try {
      const response = await scraperApi.getStatus();
      if (response.success) {
        setStatus(response.data);
      }
    } catch (error) {
      console.error('Error loading status:', error);
    }
  };

  const handleScraping = async () => {
    setIsScraping(true);
    setError(null);
    setScrapingResult(null);

    try {
      const response = await scraperApi.triggerScraping(
        selectedWebsite,
        selectedCategory || undefined
      );
      
      if (response.success) {
        setScrapingResult(response.data);
        // Reload status after scraping
        await loadStatus();
      } else {
        setError(response.error || 'Scraping failed');
      }
    } catch (error) {
      setError('Failed to start scraping');
      console.error('Scraping error:', error);
    } finally {
      setIsScraping(false);
    }
  };

  const getCategoriesForWebsite = () => {
    if (selectedWebsite === 'all') {
      return ['hookah', 'bowl', 'hose', 'hmd'];
    }
    const website = websites.find(w => w.name === selectedWebsite);
    return website?.categories || [];
  };

  return (
    <div className="card">
      <h3>🕷️ Product Scraper</h3>
      
      {/* Status Display */}
      {status && (
        <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <h4>Database Status</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
            <div>
              <strong>Total Products:</strong> {status.total_products}
            </div>
            <div>
              <strong>Categories:</strong> {status.categories}
            </div>
            <div>
              <strong>Brands:</strong> {status.brands}
            </div>
            <div>
              <strong>Websites:</strong> {status.websites}
            </div>
          </div>
        </div>
      )}

      {/* Scraping Controls */}
      <div style={{ marginBottom: '1rem' }}>
        <div className="filter-group">
          <label htmlFor="website-select">Select Website:</label>
          <select
            id="website-select"
            value={selectedWebsite}
            onChange={(e) => setSelectedWebsite(e.target.value)}
          >
            <option value="all">All Websites</option>
            {websites.map((website) => (
              <option key={website.name} value={website.name}>
                {website.display_name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="category-select">Category (Optional):</label>
          <select
            id="category-select"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            {getCategoriesForWebsite().map((category) => (
              <option key={category} value={category}>
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <button
          className="btn"
          onClick={handleScraping}
          disabled={isScraping}
          style={{ marginTop: '1rem' }}
        >
          {isScraping ? '🔄 Scraping...' : '🚀 Start Scraping'}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Results Display */}
      {scrapingResult && (
        <div className="success">
          <h4>✅ Scraping Complete!</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div>
              <strong>Products Found:</strong> {scrapingResult.products_found}
            </div>
            <div>
              <strong>Website:</strong> {scrapingResult.website}
            </div>
            {scrapingResult.category && (
              <div>
                <strong>Category:</strong> {scrapingResult.category}
              </div>
            )}
            {scrapingResult.details && (
              <>
                <div>
                  <strong>Added:</strong> {scrapingResult.details.added || 0}
                </div>
                <div>
                  <strong>Updated:</strong> {scrapingResult.details.updated || 0}
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Website Information */}
      <div style={{ marginTop: '2rem' }}>
        <h4>📋 Available Websites</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
          {websites.map((website) => (
            <div key={website.name} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1rem' }}>
              <h5>{website.display_name}</h5>
              <p style={{ fontSize: '0.9rem', color: '#666' }}>
                <a href={website.url} target="_blank" rel="noopener noreferrer">
                  {website.url}
                </a>
              </p>
              <div style={{ marginTop: '0.5rem' }}>
                <strong>Categories:</strong> {website.categories.join(', ')}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScraperManager; 