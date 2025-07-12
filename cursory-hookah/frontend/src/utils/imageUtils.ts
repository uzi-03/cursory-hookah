/**
 * Utility functions for image handling and validation
 */

export interface ImageValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Validates if a URL is a valid image URL
 */
export const validateImageUrl = (url?: string): ImageValidationResult => {
  if (!url) {
    return { isValid: false, error: 'No URL provided' };
  }

  try {
    const urlObj = new URL(url);
    
    // Check if it's a valid HTTP/HTTPS URL
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      return { isValid: false, error: 'Invalid protocol' };
    }

    // Check for common image file extensions
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
    const hasImageExtension = imageExtensions.some(ext => 
      urlObj.pathname.toLowerCase().includes(ext)
    );

    if (!hasImageExtension) {
      console.warn(`⚠️ URL may not be an image: ${url}`);
    }

    return { isValid: true };
  } catch (error) {
    return { isValid: false, error: 'Invalid URL format' };
  }
};

/**
 * Preloads an image to check if it loads successfully
 */
export const preloadImage = (src: string): Promise<boolean> => {
  return new Promise((resolve) => {
    const img = new Image();
    
    img.onload = () => {
      console.log(`✅ Image preloaded successfully: ${src}`);
      resolve(true);
    };
    
    img.onerror = () => {
      console.warn(`⚠️ Failed to preload image: ${src}`);
      resolve(false);
    };
    
    img.src = src;
  });
};

/**
 * Generates a placeholder image URL based on product name
 */
export const generatePlaceholderUrl = (productName: string): string => {
  // Use a placeholder service like placehold.co
  const encodedName = encodeURIComponent(productName);
  return `https://placehold.co/400x300/f8f9fa/6c757d?text=${encodedName}`;
};

/**
 * Sanitizes image URLs to prevent XSS and other security issues
 */
export const sanitizeImageUrl = (url?: string): string | undefined => {
  if (!url) return undefined;
  
  try {
    const urlObj = new URL(url);
    
    // Only allow HTTP/HTTPS protocols
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      console.warn(`⚠️ Blocked non-HTTP URL: ${url}`);
      return undefined;
    }
    
    // Check for potentially malicious domains (basic check)
    const suspiciousPatterns = ['javascript:', 'data:', 'vbscript:'];
    if (suspiciousPatterns.some(pattern => url.toLowerCase().includes(pattern))) {
      console.warn(`⚠️ Blocked suspicious URL: ${url}`);
      return undefined;
    }
    
    return url;
  } catch (error) {
    console.warn(`⚠️ Invalid URL format: ${url}`);
    return undefined;
  }
};

/**
 * Gets the optimal image size based on container dimensions
 */
export const getOptimalImageSize = (containerWidth: number, containerHeight: number): string => {
  // For now, return the original size
  // In a real app, you might want to use different sizes for different devices
  return `${containerWidth}x${containerHeight}`;
}; 