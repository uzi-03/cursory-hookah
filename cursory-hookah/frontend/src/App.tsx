import React, { useState, useEffect } from 'react';
import { Gear, UserGear, FilterOptions } from './types';
import { gearApi, userApi, recommendationsApi } from './services/api';
import GearCard from './components/GearCard';
import GearFilters from './components/GearFilters';

function App() {
  const [allGear, setAllGear] = useState<Gear[]>([]);
  const [userGear, setUserGear] = useState<UserGear[]>([]);
  const [recommendations, setRecommendations] = useState<Gear[]>([]);
  const [filters, setFilters] = useState<FilterOptions>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'browse' | 'collection' | 'recommendations'>('browse');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (activeTab === 'browse') {
      loadGear();
    } else if (activeTab === 'recommendations') {
      loadRecommendations();
    }
  }, [activeTab, filters]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [gearResponse, userGearResponse] = await Promise.all([
        gearApi.getAll(),
        userApi.getUserGear()
      ]);

      if (gearResponse.success) {
        setAllGear(gearResponse.data);
      }

      if (userGearResponse.success) {
        setUserGear(userGearResponse.data);
      }
    } catch (error) {
      setError('Failed to load initial data');
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadGear = async () => {
    try {
      setLoading(true);
      const response = await gearApi.getAll(filters);
      if (response.success) {
        setAllGear(response.data);
      }
    } catch (error) {
      setError('Failed to load gear');
      console.error('Error loading gear:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const response = await recommendationsApi.getRecommendations();
      if (response.success) {
        setRecommendations(response.data);
      }
    } catch (error) {
      setError('Failed to load recommendations');
      console.error('Error loading recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCollection = async (gearId: number) => {
    try {
      const response = await userApi.addGearToUser(gearId);
      if (response.success) {
        // Reload user gear
        const userGearResponse = await userApi.getUserGear();
        if (userGearResponse.success) {
          setUserGear(userGearResponse.data);
        }
      }
    } catch (error) {
      setError('Failed to add gear to collection');
      console.error('Error adding gear to collection:', error);
    }
  };

  const handleRemoveFromCollection = async (gearId: number) => {
    try {
      const response = await userApi.removeGearFromUser(gearId);
      if (response.success) {
        // Reload user gear
        const userGearResponse = await userApi.getUserGear();
        if (userGearResponse.success) {
          setUserGear(userGearResponse.data);
        }
      }
    } catch (error) {
      setError('Failed to remove gear from collection');
      console.error('Error removing gear from collection:', error);
    }
  };

  const isInCollection = (gearId: number) => {
    return userGear.some(ug => ug.gear_id === gearId);
  };

  const renderGearList = (gearList: Gear[], title: string) => {
    if (loading) {
      return <div className="loading">Loading {title.toLowerCase()}...</div>;
    }

    if (error) {
      return <div className="error">{error}</div>;
    }

    if (gearList.length === 0) {
      return (
        <div className="empty-state">
          <h3>No {title.toLowerCase()} found</h3>
          <p>Try adjusting your filters or adding some gear to your collection.</p>
        </div>
      );
    }

    return (
      <div className="grid">
        {gearList.map((gear) => (
          <GearCard
            key={gear.id}
            gear={gear}
            onAddToCollection={handleAddToCollection}
            onRemoveFromCollection={handleRemoveFromCollection}
            isInCollection={isInCollection(gear.id)}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>🚬 Cursory Hookah</h1>
          <p style={{ textAlign: 'center', color: '#666', marginTop: '0.5rem' }}>
            Discover compatible gear and accessories for your hookah setup
          </p>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          {/* Navigation Tabs */}
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
            <button
              className={`btn ${activeTab === 'browse' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveTab('browse')}
            >
              Browse All Gear
            </button>
            <button
              className={`btn ${activeTab === 'collection' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveTab('collection')}
            >
              My Collection ({userGear.length})
            </button>
            <button
              className={`btn ${activeTab === 'recommendations' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveTab('recommendations')}
            >
              Recommendations
            </button>
          </div>

          {/* Filters - only show for browse tab */}
          {activeTab === 'browse' && (
            <GearFilters
              currentFilters={filters}
              onFiltersChange={setFilters}
            />
          )}

          {/* User Collection */}
          {activeTab === 'collection' && (
            <div className="user-gear">
              <h3>My Hookah Collection</h3>
              {userGear.length === 0 ? (
                <div className="empty-state">
                  <h3>Your collection is empty</h3>
                  <p>Start by browsing gear and adding items to your collection!</p>
                  <button className="btn" onClick={() => setActiveTab('browse')}>
                    Browse Gear
                  </button>
                </div>
              ) : (
                <div className="grid">
                  {userGear.map((userGearItem) => (
                    userGearItem.gear && (
                      <GearCard
                        key={userGearItem.id}
                        gear={userGearItem.gear}
                        onRemoveFromCollection={handleRemoveFromCollection}
                        isInCollection={true}
                      />
                    )
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Browse All Gear */}
          {activeTab === 'browse' && renderGearList(allGear, 'Gear')}

          {/* Recommendations */}
          {activeTab === 'recommendations' && renderGearList(recommendations, 'Recommendations')}
        </div>
      </main>
    </div>
  );
}

export default App; 