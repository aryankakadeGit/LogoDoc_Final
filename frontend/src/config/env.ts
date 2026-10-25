// Reads build-time settings from .env (VITE_* variables) with safe defaults.

const DEFAULT_API_BASE_URL = "http://localhost:8000";

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL).replace(/\/+$/, "");

export const MAX_UPLOAD_MB = Number(import.meta.env.VITE_MAX_UPLOAD_MB) || 5;
export const MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024;

// Analysis can take up to ~2 minutes in the worst case (AI retries), so wait a bit longer.
export const ANALYZE_TIMEOUT_MS = 180_000;
// Recommendation calls are one AI text call each.
export const RECOMMENDATION_TIMEOUT_MS = 120_000;
