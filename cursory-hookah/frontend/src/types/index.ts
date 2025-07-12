export interface Gear {
  id: number;
  name: string;
  category: string;
  brand: string;
  model?: string;
  description?: string;
  price?: number;
  image_url?: string;
  product_url?: string;
  specifications?: Record<string, any>;
  compatibility_tags?: string[];
  rating: number;
  review_count: number;
  source_website?: string;
  created_at?: string;
  updated_at?: string;
}

export interface UserGear {
  id: number;
  user_id: number;
  gear_id: number;
  gear?: Gear;
  added_at?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  count?: number;
  message?: string;
  error?: string;
}

export interface RecommendationsResponse {
  success: boolean;
  data: Gear[];
  count: number;
  type: 'compatible' | 'popular';
  user_gear_count: number;
}

export interface ScrapingStatus {
  total_products: number;
  categories: number;
  brands: number;
  websites: number;
  last_updated: string;
}

export interface Website {
  name: string;
  display_name: string;
  url: string;
  categories: string[];
}

export interface FilterOptions {
  category?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
} 