import React from 'react';
import { Gear } from '../types';

interface GearCardProps {
  gear: Gear;
  onAddToCollection?: (gearId: number) => void;
  onRemoveFromCollection?: (gearId: number) => void;
  isInCollection?: boolean;
}

const GearCard: React.FC<GearCardProps> = ({ 
  gear, 
  onAddToCollection, 
  onRemoveFromCollection, 
  isInCollection = false 
}) => {
  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i}>★</span>);
    }
    
    if (hasHalfStar) {
      stars.push(<span key="half">☆</span>);
    }
    
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`}>☆</span>);
    }
    
    return stars;
  };

  return (
    <div className="gear-item">
      <div className="gear-image">
        {gear.image_url ? (
          <img src={gear.image_url} alt={gear.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        ) : (
          <span>No Image Available</span>
        )}
      </div>
      
      <div className="gear-content">
        <h3 className="gear-title">{gear.name}</h3>
        <p className="gear-brand">{gear.brand}</p>
        
        {gear.price && (
          <p className="gear-price">${gear.price.toFixed(2)}</p>
        )}
        
        <div className="gear-rating">
          <span className="stars">{renderStars(gear.rating)}</span>
          <span>({gear.review_count} reviews)</span>
        </div>
        
        {gear.description && (
          <p className="gear-description">{gear.description}</p>
        )}
        
        {gear.compatibility_tags && gear.compatibility_tags.length > 0 && (
          <div className="gear-tags">
            {gear.compatibility_tags.slice(0, 3).map((tag, index) => (
              <span key={index} className="tag">{tag}</span>
            ))}
            {gear.compatibility_tags.length > 3 && (
              <span className="tag">+{gear.compatibility_tags.length - 3} more</span>
            )}
          </div>
        )}
        
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
          {isInCollection ? (
            <button 
              className="btn btn-danger"
              onClick={() => onRemoveFromCollection?.(gear.id)}
            >
              Remove from Collection
            </button>
          ) : (
            <button 
              className="btn"
              onClick={() => onAddToCollection?.(gear.id)}
            >
              Add to Collection
            </button>
          )}
          
          {gear.product_url && (
            <a 
              href={gear.product_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn btn-secondary"
            >
              View Product
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default GearCard; 