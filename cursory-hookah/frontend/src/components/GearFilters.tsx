import React, { useState, useEffect } from 'react';
import { gearApi } from '../services/api';
import { FilterOptions } from '../types';

interface GearFiltersProps {
  onFiltersChange: (filters: FilterOptions) => void;
  currentFilters: FilterOptions;
}

const GearFilters: React.FC<GearFiltersProps> = ({ onFiltersChange, currentFilters }) => {
  const [categories, setCategories] = useState<string[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFilterOptions = async () => {
      try {
        const [categoriesResponse, brandsResponse] = await Promise.all([
          gearApi.getCategories(),
          gearApi.getBrands()
        ]);

        if (categoriesResponse.success) {
          setCategories(categoriesResponse.data);
        }

        if (brandsResponse.success) {
          setBrands(brandsResponse.data);
        }
      } catch (error) {
        console.error('Error loading filter options:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFilterOptions();
  }, []);

  const handleFilterChange = (key: keyof FilterOptions, value: string | number | undefined) => {
    const newFilters = { ...currentFilters };
    
    if (value === '' || value === undefined) {
      delete newFilters[key];
    } else {
      newFilters[key] = value as any;
    }
    
    onFiltersChange(newFilters);
  };

  if (loading) {
    return <div className="loading">Loading filters...</div>;
  }

  return (
    <div className="filters">
      <h3>Filter Gear</h3>
      
      <div className="filter-group">
        <label htmlFor="category">Category</label>
        <select
          id="category"
          value={currentFilters.category || ''}
          onChange={(e) => handleFilterChange('category', e.target.value || undefined)}
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="brand">Brand</label>
        <select
          id="brand"
          value={currentFilters.brand || ''}
          onChange={(e) => handleFilterChange('brand', e.target.value || undefined)}
        >
          <option value="">All Brands</option>
          {brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="min-price">Minimum Price</label>
        <input
          id="min-price"
          type="number"
          placeholder="0"
          value={currentFilters.min_price || ''}
          onChange={(e) => handleFilterChange('min_price', e.target.value ? parseFloat(e.target.value) : undefined)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="max-price">Maximum Price</label>
        <input
          id="max-price"
          type="number"
          placeholder="1000"
          value={currentFilters.max_price || ''}
          onChange={(e) => handleFilterChange('max_price', e.target.value ? parseFloat(e.target.value) : undefined)}
        />
      </div>

      <button
        className="btn btn-secondary"
        onClick={() => onFiltersChange({})}
      >
        Clear Filters
      </button>
    </div>
  );
};

export default GearFilters; 