import axios from 'axios';
import { Gear, UserGear, ApiResponse, RecommendationsResponse, ScrapingStatus, FilterOptions, Website } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Gear API calls
export const gearApi = {
  getAll: async (filters?: FilterOptions): Promise<ApiResponse<Gear[]>> => {
    const params = new URLSearchParams();
    if (filters?.category) params.append('category', filters.category);
    if (filters?.brand) params.append('brand', filters.brand);
    if (filters?.min_price) params.append('min_price', filters.min_price.toString());
    if (filters?.max_price) params.append('max_price', filters.max_price.toString());
    
    const response = await api.get(`/gear/?${params.toString()}`);
    return response.data;
  },

  getById: async (id: number): Promise<ApiResponse<Gear>> => {
    const response = await api.get(`/gear/${id}`);
    return response.data;
  },

  getCategories: async (): Promise<ApiResponse<string[]>> => {
    const response = await api.get('/gear/categories');
    return response.data;
  },

  getBrands: async (): Promise<ApiResponse<string[]>> => {
    const response = await api.get('/gear/brands');
    return response.data;
  },
};

// User API calls
export const userApi = {
  getUserGear: async (): Promise<ApiResponse<UserGear[]>> => {
    const response = await api.get('/user/gear');
    return response.data;
  },

  addGearToUser: async (gearId: number): Promise<ApiResponse<UserGear>> => {
    const response = await api.post('/user/gear', { gear_id: gearId });
    return response.data;
  },

  removeGearFromUser: async (gearId: number): Promise<ApiResponse<{}>> => {
    const response = await api.delete(`/user/gear/${gearId}`);
    return response.data;
  },
};

// Recommendations API calls
export const recommendationsApi = {
  getRecommendations: async (): Promise<RecommendationsResponse> => {
    const response = await api.get('/recommendations/');
    return response.data;
  },

  getCategoryRecommendations: async (category: string): Promise<ApiResponse<Gear[]>> => {
    const response = await api.get(`/recommendations/category/${category}`);
    return response.data;
  },
};

// Scraper API calls
export const scraperApi = {
  triggerScraping: async (website?: string, category?: string): Promise<ApiResponse<{ products_found: number; website: string; category?: string; details?: any }>> => {
    const response = await api.post('/scraper/trigger', { 
      website: website || 'demo',
      category: category
    });
    return response.data;
  },

  getStatus: async (): Promise<ApiResponse<ScrapingStatus>> => {
    const response = await api.get('/scraper/status');
    return response.data;
  },

  getWebsites: async (): Promise<ApiResponse<Website[]>> => {
    const response = await api.get('/scraper/websites');
    return response.data;
  },
}; 