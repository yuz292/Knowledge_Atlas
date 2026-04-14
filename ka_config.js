/**
 * Knowledge Atlas — Site Configuration
 * =====================================
 * Include this script BEFORE any page-specific scripts to set the API
 * base URL for the current environment.
 *
 * Local dev:   Leave as-is (defaults to localhost:8765)
 * Production:  Change apiBase to the university VM address
 *
 * Usage in HTML:
 *   Load ka_config.js before your page-specific script.
 *
 * All KA pages read from window.__KA_CONFIG__.apiBase with a fallback
 * to 'http://localhost:8765' if this file is not loaded.
 */
window.__KA_CONFIG__ = {
  // ── Change this for production deployment ──
  apiBase: '',  // empty = same origin (API and pages on same port)

  // ── Other site-wide settings ──
  siteName: 'Knowledge Atlas',
  courseCode: 'COGS 160',
  quarter: 'Spring 2026',
};
