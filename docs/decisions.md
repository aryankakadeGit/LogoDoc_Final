# Decisions Log

- Stack finalized: React/TS/Vite/Tailwind + FastAPI/Pydantic + Gemini Flash (free tier).
- No database, no image storage for MVP.
- Formats: PNG, JPG/JPEG, WebP, SVG (SVG sanitized + rasterized to PNG on backend).
- Overall score = arithmetic mean of 11 parameter scores, calculated by backend.
- Logo Status = separate module (logo_status). MVP: AI brand recognition + generic elements,
  no extra AI call. Never claims "100% original"; shows sources checked + "not a trademark search".
  Phase 2: Google Cloud Vision Web Detection / Logo Detection via a new checker.
- Recommendations split into ai_generated and manual_design, sharing a common analysis summary.
  The .txt download lives in manual_design (export module removed).
- Privacy notice on upload (Gemini free tier may use inputs to improve products).
- Planned upgrades: Gemini paid tier, Cloud Vision logo detection, optional PostgreSQL.
