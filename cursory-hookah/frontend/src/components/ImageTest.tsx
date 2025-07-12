import React from 'react';
import ProductImage from './ProductImage';

const ImageTest: React.FC = () => {
  const testImages = [
    {
      name: 'Valid Image',
      url: 'https://via.placeholder.com/400x300/667eea/ffffff?text=Valid+Image',
      description: 'This should load successfully'
    },
    {
      name: 'Invalid URL',
      url: 'https://invalid-url-that-does-not-exist.com/image.jpg',
      description: 'This should show fallback'
    },
    {
      name: 'No URL',
      url: undefined,
      description: 'This should show placeholder'
    },
    {
      name: 'Malicious URL',
      url: 'javascript:alert("xss")',
      description: 'This should be blocked'
    }
  ];

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Image Loading Test</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
        {testImages.map((test, index) => (
          <div key={index} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1rem' }}>
            <h3>{test.name}</h3>
            <p>{test.description}</p>
            <div style={{ height: '200px', width: '100%' }}>
              <ProductImage 
                src={test.url} 
                alt={test.name}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
            <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.5rem' }}>
              URL: {test.url || 'undefined'}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageTest; 