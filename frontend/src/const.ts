export const COOKIE_NAME = "session";
export const ONE_YEAR_MS = 365 * 24 * 60 * 60 * 1000;

export const APP_TITLE = "Stride Ahead Events Platform";

export const APP_LOGO = "https://placehold.co/128x128/E1E7EF/1F2937?text=App";

// Generate login URL at runtime
export const getLoginUrl = () => {
  return "#"; // Placeholder for FastAPI auth
};
