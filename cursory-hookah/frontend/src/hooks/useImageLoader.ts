import { useState, useEffect, useCallback } from 'react';
import { preloadImage, validateImageUrl, sanitizeImageUrl } from '../utils/imageUtils';

interface UseImageLoaderReturn {
  isLoading: boolean;
  hasError: boolean;
  isValidUrl: boolean;
  sanitizedUrl: string | undefined;
  retry: () => void;
}

export const useImageLoader = (src?: string): UseImageLoaderReturn => {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [isValidUrl, setIsValidUrl] = useState(false);
  const [sanitizedUrl, setSanitizedUrl] = useState<string | undefined>(undefined);

  const validateAndSanitize = useCallback(async () => {
    if (!src) {
      setIsLoading(false);
      setHasError(true);
      setIsValidUrl(false);
      return;
    }

    // Validate URL format
    const validation = validateImageUrl(src);
    if (!validation.isValid) {
      console.warn(`⚠️ Invalid image URL: ${validation.error}`);
      setIsLoading(false);
      setHasError(true);
      setIsValidUrl(false);
      return;
    }

    // Sanitize URL
    const sanitized = sanitizeImageUrl(src);
    if (!sanitized) {
      console.warn(`⚠️ URL sanitization failed: ${src}`);
      setIsLoading(false);
      setHasError(true);
      setIsValidUrl(false);
      return;
    }

    setSanitizedUrl(sanitized);
    setIsValidUrl(true);

    // Preload image to check if it actually loads
    try {
      const loadSuccess = await preloadImage(sanitized);
      if (loadSuccess) {
        setIsLoading(false);
        setHasError(false);
      } else {
        setIsLoading(false);
        setHasError(true);
      }
    } catch (error) {
      console.error(`❌ Error preloading image: ${error}`);
      setIsLoading(false);
      setHasError(true);
    }
  }, [src]);

  const retry = useCallback(() => {
    setIsLoading(true);
    setHasError(false);
    validateAndSanitize();
  }, [validateAndSanitize]);

  useEffect(() => {
    validateAndSanitize();
  }, [validateAndSanitize]);

  return {
    isLoading,
    hasError,
    isValidUrl,
    sanitizedUrl,
    retry
  };
}; 