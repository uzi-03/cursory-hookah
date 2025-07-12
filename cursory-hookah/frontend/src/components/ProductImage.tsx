import React, { useState, useCallback } from 'react';
import { useImageLoader } from '../hooks/useImageLoader';

interface ProductImageProps {
  src?: string;
  alt: string;
  className?: string;
  style?: React.CSSProperties;
}

const ProductImage: React.FC<ProductImageProps> = ({ 
  src, 
  alt, 
  className = '', 
  style = {} 
}) => {
  const { isLoading, hasError, sanitizedUrl, retry } = useImageLoader(src);
  const [imageState, setImageState] = useState<'loading' | 'loaded' | 'error'>('loading');

  const handleImageLoad = useCallback(() => {
    setImageState('loaded');
    console.log(`✅ Image loaded successfully: ${alt}`);
  }, [alt]);

  const handleImageError = useCallback(() => {
    setImageState('error');
    console.warn(`⚠️ Failed to load image for: ${alt}`);
    retry();
  }, [alt, retry]);

  // Default fallback image - a placeholder with hookah gear icon
  const renderFallbackImage = () => (
    <div 
      className={`gear-image-placeholder ${className}`}
      style={{
        ...style,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
        color: '#6c757d',
        fontSize: '2rem',
        fontWeight: 'bold',
        border: '2px dashed #dee2e6',
        borderRadius: '8px',
        position: 'relative'
      }}
    >
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🚬</div>
        <div style={{ fontSize: '0.9rem', fontWeight: '600' }}>Hookah Gear</div>
        <div style={{ fontSize: '0.7rem', opacity: 0.7, marginTop: '0.25rem' }}>Image Unavailable</div>
      </div>
    </div>
  );

  // Loading state
  if (isLoading && sanitizedUrl) {
    return (
      <div 
        className={`gear-image-loading ${className}`}
        style={{
          ...style,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%)',
          color: '#6c757d',
          fontSize: '0.9rem',
          borderRadius: '8px'
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🚬</div>
          <div style={{ fontSize: '0.8rem', fontWeight: '600' }}>Loading Gear...</div>
        </div>
      </div>
    );
  }

  // Error state or no image URL
  if (hasError || !sanitizedUrl) {
    return renderFallbackImage();
  }

  // Successfully loaded image
  return (
    <img
      src={sanitizedUrl}
      alt={alt}
      className={className}
      style={{
        ...style,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        borderRadius: '8px 8px 0 0'
      }}
      onLoad={handleImageLoad}
      onError={handleImageError}
      loading="lazy"
      crossOrigin="anonymous"
    />
  );
};

export default ProductImage; 